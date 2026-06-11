from __future__ import annotations

import _thread
import multiprocessing as mp
import pickle
import queue
import socket
import sys
import time
import warnings
from collections.abc import Callable
from contextlib import suppress
from multiprocessing.connection import Connection
from multiprocessing.synchronize import Event as MultiprocessingEvent
from pathlib import Path
from threading import Event, Thread
from typing import Any

from .. import core, helpers, optional_features
from ..logging import log
from ..server import Server
from . import native, window_icon
from .event_manager import event_manager

with suppress(ImportError):
    with warnings.catch_warnings():
        # webview depends on bottle which uses the deprecated CGI function (https://github.com/bottlepy/bottle/issues/1403)
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        import webview
        import webview.dom
    optional_features.register('webview')


def _open_window(
    protocol: str, host: str, port: int, title: str, width: int, height: int, fullscreen: bool, frameless: bool,
    method_queue: mp.Queue, response_queue: mp.Queue, event_sender: Connection,
    favicon: str | Path | None = None,
    window_args: dict[str, Any] | None = None,
    settings: dict[str, Any] | None = None,
    start_args: dict[str, Any] | None = None,
    dropped_keys: dict[str, list[str]] | None = None,
) -> None:
    while not helpers.is_port_open(host, port):
        time.sleep(0.1)

    # Let re-imported values win over the parent's picklable subset, so previous behavior is preserved (#6082).
    window_args = {**(window_args or {}), **core.app.native.window_args}
    settings = {**(settings or {}), **core.app.native.settings}
    start_args = {**(start_args or {}), **core.app.native.start_args}

    # Warn only about keys the parent could not pickle AND re-import did not restore here, i.e. that are truly lost.
    for name, merged in [('window_args', window_args), ('settings', settings), ('start_args', start_args)]:
        for key in (dropped_keys or {}).get(name, []):
            if key not in merged:
                helpers.warn_once(
                    f'Could not forward app.native.{name}["{key}"] to the native window process '
                    'because it is not picklable, so it is ignored. '
                    'See https://github.com/zauberzeug/nicegui/issues/6082 for details.'
                )

    window_kwargs = {
        'url': helpers.format_url(protocol, host, port),
        'title': title,
        'width': width,
        'height': height,
        'fullscreen': fullscreen,
        'frameless': frameless,
        **window_args,
    }
    webview.settings.update(**settings)
    window = webview.create_window(**window_kwargs)
    assert window is not None
    closed = Event()
    window.events.closed += closed.set
    _bind_pywebview_events(window, event_sender)

    if sys.platform == 'win32' and favicon is not None:
        def on_shown() -> None:
            window_icon.apply_icon(window.native.Handle.ToInt32(), title, str(favicon))
            window.events.shown -= on_shown
        window.events.shown += on_shown

    _start_window_method_executor(window, method_queue, response_queue, closed)
    _warn_if_esm_unsupported(window)
    webview.start(**start_args)


def _bind_pywebview_events(window: webview.Window, event_sender: Connection) -> None:
    def send(event_type: str, **kwargs: Any) -> None:
        try:
            event_sender.send({'type': event_type, 'args': kwargs})
        except OSError:
            pass

    def bind_drop() -> None:
        window.evaluate_js('''
            document.addEventListener("dragover", function(e) {
              if (e.dataTransfer && e.dataTransfer.types.indexOf("Files") >= 0) e.preventDefault();
            });
        ''')
        window.dom.document.events.drop += \
            webview.dom.DOMEventHandler(lambda e: send('drop', files=[  # type: ignore[arg-type]
                file_.get('pywebviewFullPath', '') for file_ in e.get('dataTransfer', {}).get('files', [])
            ]), True, False)

    window.events.shown += lambda: send('shown')
    window.events.loaded += lambda: send('loaded')
    window.events.loaded += bind_drop
    window.events.minimized += lambda: send('minimized')
    window.events.maximized += lambda: send('maximized')
    window.events.restored += lambda: send('restored')
    window.events.resized += lambda width, height: send('resized', width=width, height=height)
    window.events.moved += lambda x, y: send('moved', x=x, y=y)
    window.events.closed += lambda: send('closed')
    # 'closing' is not bridged yet — it requires a synchronous round-trip to support vetoing the close


def _start_window_method_executor(window: webview.Window,
                                  method_queue: mp.Queue,
                                  response_queue: mp.Queue,
                                  closed: Event) -> None:
    def execute(method: Callable, args: tuple[Any, ...], kwargs: dict[str, Any]) -> None:
        try:
            response = method(*args, **kwargs)
            if response is not None or 'dialog' in method.__name__:
                response_queue.put(response)
        except Exception:
            log.exception(f'error in window.{method.__name__}')

    def window_method_executor() -> None:
        pending_executions: list[Thread] = []
        while not closed.is_set():
            try:
                method_name, args, kwargs = method_queue.get(block=False)
                if method_name == 'signal_server_shutdown':
                    if pending_executions:
                        log.warning('shutdown is possibly blocked by opened dialogs like a file picker')
                        while pending_executions:
                            pending_executions.pop().join()
                elif method_name == 'get_always_on_top':
                    response_queue.put(window.on_top)
                elif method_name == 'set_always_on_top':
                    window.on_top = args[0]
                elif method_name == 'get_position':
                    response_queue.put((int(window.x), int(window.y)))
                elif method_name == 'get_size':
                    response_queue.put((int(window.width), int(window.height)))
                else:
                    method = getattr(window, method_name)
                    if callable(method):
                        pending_executions.append(Thread(target=execute, args=(method, args, kwargs)))
                        pending_executions[-1].start()
                    else:
                        log.error(f'window.{method_name} is not callable')
            except queue.Empty:
                time.sleep(0.016)  # avoid issue https://github.com/zauberzeug/nicegui/issues/2482 on Windows
            except Exception:
                log.exception(f'error in window.{method_name}')

    Thread(target=window_method_executor).start()


def _warn_if_esm_unsupported(window: webview.Window) -> None:
    """Log an error after page load if the browser engine lacks ES module / import map support."""
    def check() -> None:
        if not window.evaluate_js('typeof Vue !== "undefined"'):
            log.error(
                'Vue failed to load, and NiceGUI critically relies on it. '
                'This typically means the webview browser engine does not support import maps (requires Chrome 89+). '
                'On Linux, ensure you have a modern browser engine — e.g. an up-to-date WebKitGTK or Qt-based backend.',
            )

    window.events.loaded += check


def activate(protocol: str, host: str, port: int, title: str, width: int, height: int, fullscreen: bool, frameless: bool,
             shutdown_event: MultiprocessingEvent | None = None,
             favicon: str | Path | None = None) -> None:
    """Activate native mode."""
    def check_shutdown() -> None:
        while process.is_alive():
            time.sleep(0.1)
        if shutdown_event is not None:
            shutdown_event.set()
        Server.instance.should_exit = True
        while not core.app.is_stopped:
            time.sleep(0.1)
        _thread.interrupt_main()
        event_manager.stop()
        native.remove_queues()

    if not optional_features.has('webview'):
        log.error('Native mode is not supported in this configuration.\n'
                  'Please run "pip install pywebview" to use it.')
        sys.exit(1)

    mp.freeze_support()
    native.create_queues()
    event_manager.start()
    window_args, dropped_window_args = _split_picklable(core.app.native.window_args)
    settings, dropped_settings = _split_picklable(core.app.native.settings)
    start_args, dropped_start_args = _split_picklable(core.app.native.start_args)
    dropped_keys = {'window_args': dropped_window_args, 'settings': dropped_settings, 'start_args': dropped_start_args}
    args = (protocol, host, port, title, width, height, fullscreen, frameless,
            native.method_queue, native.response_queue, native.event_sender, favicon,
            window_args, settings, start_args, dropped_keys)
    process = native.SPAWN_CONTEXT.Process(target=_open_window, args=args, daemon=True)
    process.start()

    Thread(target=check_shutdown, daemon=True).start()


def _split_picklable(config: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Split a native config dict into its picklable items and the keys that cannot cross the spawn boundary."""
    picklable: dict[str, Any] = {}
    dropped: list[str] = []
    for key, value in config.items():
        try:
            pickle.dumps(value)
        except Exception:  # pylint: disable=broad-except
            dropped.append(key)
        else:
            picklable[key] = value
    return picklable, dropped


def find_open_port(start_port: int = 8000, end_port: int = 8999) -> int:
    """Reliably find an open port in a given range.

    This function will actually try to open the port to ensure no firewall blocks it.
    This is better than, e.g., passing port=0 to uvicorn.
    """
    for port in range(start_port, end_port + 1):
        with suppress(OSError):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
    raise OSError('No open port found')
