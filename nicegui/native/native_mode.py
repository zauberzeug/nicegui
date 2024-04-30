from __future__ import annotations

import _thread
import multiprocessing as mp
import queue
import socket
import sys
import tempfile
import time
import warnings
from threading import Event, Thread
from typing import Any, Callable, Dict, List, Tuple

from .. import core, helpers, optional_features
from ..logging import log
from ..server import Server
from . import native

try:
    with warnings.catch_warnings():
        # webview depends on bottle which uses the deprecated CGI function (https://github.com/bottlepy/bottle/issues/1403)
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        import webview
    optional_features.register('webview')
except ModuleNotFoundError:
    pass


def _open_window(
    host: str, port: int, title: str, width: int, height: int, fullscreen: bool, frameless: bool,
    method_queue: mp.Queue, response_queue: mp.Queue,
) -> None:
    while not helpers.is_port_open(host, port):
        time.sleep(0.1)

    window_kwargs = {
        'url': f'http://{host}:{port}',
        'title': title,
        'width': width,
        'height': height,
        'fullscreen': fullscreen,
        'frameless': frameless,
        **core.app.native.window_args,
    }
    webview.settings.update(**core.app.native.settings)
    window = webview.create_window(**window_kwargs)
    closed = Event()
    window.events.closed += closed.set
    _start_window_method_executor(window, method_queue, response_queue, closed)
    webview.start(storage_path=tempfile.mkdtemp(), **core.app.native.start_args)


def _start_window_method_executor(window: webview.Window,
                                  method_queue: mp.Queue,
                                  response_queue: mp.Queue,
                                  closed: Event) -> None:
    def execute(method: Callable, args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> None:
        try:
            response = method(*args, **kwargs)
            if response is not None or 'dialog' in method.__name__:
                response_queue.put(response)
        except Exception:
            log.exception(f'error in window.{method.__name__}')

    def window_method_executor() -> None:
        pending_executions: List[Thread] = []
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
                time.sleep(0.016)  # NOTE: avoid issue https://github.com/zauberzeug/nicegui/issues/2482 on Windows
            except Exception:
                log.exception(f'error in window.{method_name}')

    Thread(target=window_method_executor).start()


def activate(host: str, port: int, title: str, width: int, height: int, fullscreen: bool, frameless: bool) -> None:
    """Activate native mode."""
    def check_shutdown() -> None:
        while process.is_alive():
            time.sleep(0.1)
        Server.instance.should_exit = True
        while not core.app.is_stopped:
            time.sleep(0.1)
        _thread.interrupt_main()

    if not optional_features.has('webview'):
        log.error('Native mode is not supported in this configuration.\n'
                  'Please run "pip install pywebview" to use it.')
        sys.exit(1)

    mp.freeze_support()
    args = host, port, title, width, height, fullscreen, frameless, native.method_queue, native.response_queue
    process = mp.Process(target=_open_window, args=args, daemon=True)
    process.start()

    Thread(target=check_shutdown, daemon=True).start()


def find_open_port(start_port: int = 8000, end_port: int = 8999) -> int:
    """Reliably find an open port in a given range.

    This function will actually try to open the port to ensure no firewall blocks it.
    This is better than, e.g., passing port=0 to uvicorn.
    """
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            pass
    raise OSError('No open port found')
