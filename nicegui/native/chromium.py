# pylint: disable=C0116
"""Fallback backend for native mode, using a browser that is already installed.

Native mode normally runs on pywebview, which embeds a platform webview and therefore needs a
platform GUI stack: pyobjc on macOS, pythonnet on Windows, WebKitGTK or QtWebEngine on Linux.
That is why it lives behind the `native` extra.

This module provides a fallback for when that extra is not installed, adding no packages beyond
what NiceGUI already installs. Instead of embedding an engine, it drives a Chromium-family
browser that is already on the machine in `--app` mode: a window with no tabs and no omnibox,
its own taskbar entry and its own lifecycle. Window control and JavaScript evaluation go over
the Chrome DevTools Protocol on loopback.

It deliberately exposes the same names `native_mode` and `native` already use from pywebview
(`create_window`, `start`, `settings`, `Window`, `FixPoint`, `dom.DOMEventHandler`), so it can
stand in without those modules growing a second code path.

Its fidelity is lower than pywebview's on purpose - see `UNSUPPORTED_METHODS` below - so prefer
`pip install nicegui[native]` when a real embedded window matters.
"""
from __future__ import annotations

import atexit
import json
import os
import queue
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from contextlib import suppress
from enum import IntEnum, IntFlag
from pathlib import Path
from types import SimpleNamespace
from typing import IO, Any

from .. import helpers
from ..logging import log

BROWSER_ENV_VAR = 'NICEGUI_NATIVE_BROWSER'

_CANDIDATES: dict[str, list[str]] = {
    'darwin': [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '/Applications/Chromium.app/Contents/MacOS/Chromium',
        '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
        '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
        '/Applications/Vivaldi.app/Contents/MacOS/Vivaldi',
        '~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '~/Applications/Chromium.app/Contents/MacOS/Chromium',
    ],
    'win32': [
        # a per-user (non-admin) Chrome install lives under LOCALAPPDATA, not Program Files
        r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        r'%LOCALAPPDATA%\Chromium\Application\chrome.exe',
        r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
        r'C:\Program Files\Vivaldi\Application\vivaldi.exe',
        r'%LOCALAPPDATA%\Vivaldi\Application\vivaldi.exe',
    ],
}
_LINUX_CANDIDATES = [
    'google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser',
    'microsoft-edge', 'microsoft-edge-stable', 'brave-browser', 'vivaldi-stable',
]

# pywebview window methods this backend cannot provide. Listed explicitly so that calling one
# warns instead of raising, while a genuine typo still raises AttributeError.
UNSUPPORTED_METHODS = {
    'clear_cookies',
    'create_confirmation_dialog',
    'create_file_dialog',
    'expose',
    'load_css',
    'load_html',
    'run_js',
}


def _warn_unsupported(what: str) -> None:
    """Report something the fallback cannot do, once, pointing at the backend that can."""
    helpers.warn_once(f'the fallback native backend does not support {what}; '
                      'run "pip install nicegui[native]" to use pywebview instead')


class FileDialog(IntEnum):
    """Mirrors ``webview.FileDialog``.

    Accepted so that signatures match; this backend cannot open native file pickers.
    """

    OPEN = 10
    FOLDER = 20
    SAVE = 30


class FixPoint(IntFlag):
    """Mirrors ``webview.window.FixPoint``.

    Accepted for signature compatibility; the DevTools Protocol always anchors a resize at the
    window's top-left, so the flag cannot be honoured.
    """

    NORTH = 1
    WEST = 2
    SOUTH = 4
    EAST = 8


class DOMEventHandler:
    """Mirrors ``webview.dom.DOMEventHandler``.

    Handlers are accepted and never invoked: a browser cannot hand us the filesystem paths of
    dropped files the way an embedded webview can.
    """

    def __init__(self, callback: Callable, prevent_default: bool = False, stop_propagation: bool = False) -> None:
        self.callback = callback
        self.prevent_default = prevent_default
        self.stop_propagation = stop_propagation


# pywebview's pre-5.x aliases, still referenced by native.py as default argument values
OPEN_DIALOG = FileDialog.OPEN
FOLDER_DIALOG = FileDialog.FOLDER
SAVE_DIALOG = FileDialog.SAVE

dom = SimpleNamespace(DOMEventHandler=DOMEventHandler)

settings: dict[str, Any] = {}


def find_browser() -> str | None:
    """Return the path of an installed Chromium-family browser, or ``None`` if there is none."""
    if override := os.environ.get(BROWSER_ENV_VAR):
        override = os.path.expandvars(os.path.expanduser(override))
        if Path(override).exists():
            return override
        if found := shutil.which(override):
            return found
        log.warning(f'{BROWSER_ENV_VAR} is set to "{override}", but no such browser was found')
        return None
    for candidate in _CANDIDATES.get(sys.platform, _LINUX_CANDIDATES):
        expanded = os.path.expandvars(os.path.expanduser(candidate))
        if '%' not in expanded and Path(expanded).exists():
            return expanded
        if found := shutil.which(expanded):
            return found
    return None


class _EventSlot:
    """Mirrors pywebview's ``window.events.<name> += handler`` interface."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._handlers: list[Callable] = []

    def __iadd__(self, handler: Callable) -> _EventSlot:
        self._handlers.append(handler)
        return self

    def __isub__(self, handler: Callable) -> _EventSlot:
        if handler in self._handlers:
            self._handlers.remove(handler)
        return self

    def fire(self, *args: Any) -> None:
        for handler in list(self._handlers):
            try:
                handler(*args)
            except Exception:
                log.exception(f'error in native "{self.name}" handler')


class _Events:

    def __init__(self) -> None:
        self.shown = _EventSlot('shown')
        self.loaded = _EventSlot('loaded')
        self.closed = _EventSlot('closed')
        self.closing = _EventSlot('closing')
        self.minimized = _EventSlot('minimized')
        self.maximized = _EventSlot('maximized')
        self.restored = _EventSlot('restored')
        self.resized = _EventSlot('resized')
        self.moved = _EventSlot('moved')


class _DevToolsProtocol:
    """A minimal Chrome DevTools Protocol client: blocking requests, plus a reader thread."""

    def __init__(self, ws_url: str) -> None:
        # Imported lazily so that apps which never open a native window do not pay for it.
        # websockets arrives with uvicorn[standard], which requires >=10.4, while the synchronous
        # client used here was added in 11.0 - so only websockets 10.4 exactly is too old, and it
        # is reported rather than pinned, to avoid constraining a widely shared dependency.
        try:
            from websockets.sync.client import connect  # pylint: disable=import-outside-toplevel
        except ImportError as e:
            raise RuntimeError('The fallback native backend needs websockets>=11, which provides '
                               'its synchronous client. Please upgrade websockets, or run '
                               '"pip install nicegui[native]" to use pywebview instead.') from e
        self._connection = connect(ws_url, max_size=None, open_timeout=10)
        self._next_id = 0
        self._send_lock = threading.Lock()
        self._replies: dict[int, dict] = {}
        self._pending: set[int] = set()
        self._reply_ready = threading.Condition()
        self._closed = threading.Event()
        self.on_event: Callable[[str, dict], None] = lambda method, params: None
        threading.Thread(target=self._read_loop, daemon=True).start()

    def _read_loop(self) -> None:
        try:
            for raw in self._connection:
                message = json.loads(raw)
                if 'id' in message:
                    with self._reply_ready:
                        if message['id'] in self._pending:  # otherwise the caller gave up: drop it
                            self._replies[message['id']] = message
                            self._reply_ready.notify_all()
                elif 'method' in message:
                    self.on_event(message['method'], message.get('params', {}))
        except Exception:
            pass  # the browser closing tears down the socket; `closed` handling lives in Window
        finally:
            self._closed.set()
            with self._reply_ready:
                self._reply_ready.notify_all()

    def send(self, method: str, params: dict | None = None, timeout: float = 10.0) -> dict:
        """Issue a command and wait for its reply.

        Never call this from `on_event`: the reply can only be delivered by the reader thread,
        so waiting for one inside a handler that runs on that thread deadlocks.
        """
        with self._send_lock:
            self._next_id += 1
            message_id = self._next_id
            with self._reply_ready:
                self._pending.add(message_id)
            self._connection.send(json.dumps({'id': message_id, 'method': method, 'params': params or {}}))
        deadline = time.time() + timeout
        try:
            with self._reply_ready:
                while message_id not in self._replies:
                    if self._closed.is_set():
                        raise ConnectionError(f'DevTools connection closed while waiting for {method}')
                    if not self._reply_ready.wait(max(0.0, deadline - time.time())):
                        raise TimeoutError(f'DevTools timeout on {method}')
                reply = self._replies.pop(message_id)
        finally:
            with self._reply_ready:
                self._pending.discard(message_id)
        if 'error' in reply:
            raise RuntimeError(f'DevTools error on {method}: {reply["error"]}')
        return reply.get('result', {})

    def close(self) -> None:
        with suppress(Exception):
            self._connection.close()


class Window:
    """A browser window driven over the DevTools Protocol, shaped like ``webview.Window``."""

    def __init__(self, url: str = '', title: str = '', width: int = 800, height: int = 600,
                 fullscreen: bool = False, frameless: bool = False, profile_dir: str | None = None,
                 x: int | None = None, y: int | None = None, on_top: bool = False,
                 **kwargs: Any) -> None:
        self.url = url
        self._title = title
        self.fullscreen = fullscreen
        self.frameless = frameless
        self.events = _Events()
        self.dom = SimpleNamespace(document=SimpleNamespace(events=SimpleNamespace(drop=_EventSlot('drop'))))
        self.native = None  # no platform widget to hand out; pywebview exposes the real one here
        self._initial_size = (width, height)
        self._on_top = on_top
        self._protocol: _DevToolsProtocol | None = None
        self._window_id: int | None = None
        self._bounds: dict[str, Any] = {}
        self._protocol_ready = threading.Event()
        self._process: subprocess.Popen | None = None
        self._profile_dir = profile_dir
        self._log_file: IO[bytes] | None = None
        self._events: queue.Queue = queue.Queue()
        self._synthetic_load_time = 0.0
        self._bounds_checked_at = 0.0
        self._position = (x, y)
        for name, unsupported in [('frameless', frameless), ('on_top', on_top)]:
            if unsupported:
                _warn_unsupported(f'{name}=True')
        if kwargs:
            _warn_unsupported(f'the window arguments {sorted(kwargs)}')

    # -- lifecycle ---------------------------------------------------------------------------

    def _launch(self, browser: str) -> None:
        if self._profile_dir is None:
            self._profile_dir = tempfile.mkdtemp(prefix='nicegui-native-')
        width, height = self._initial_size
        arguments = [
            browser,
            f'--app={self.url}',
            f'--user-data-dir={self._profile_dir}',
            f'--window-size={width},{height}',
            '--remote-debugging-port=0',
            '--no-first-run',
            '--no-default-browser-check',
            '--disable-background-networking',
            '--disable-component-update',
            '--disable-sync',
            '--no-service-autorun',
        ]
        if self.fullscreen:
            arguments.append('--start-fullscreen')
        # Best effort for callers that use this backend directly; NiceGUI's native mode also
        # removes fallback profiles from the parent process, where app shutdown is observable.
        atexit.register(self._remove_profile)
        self._log_file = tempfile.TemporaryFile()  # pylint: disable=consider-using-with
        # the browser must outlive this call; it is terminated in destroy()
        self._process = subprocess.Popen(  # pylint: disable=consider-using-with
            arguments, stdout=subprocess.DEVNULL, stderr=self._log_file)

    def _wait_for_debugging_port(self, timeout: float = 30.0) -> int:
        assert self._profile_dir is not None
        port_file = Path(self._profile_dir) / 'DevToolsActivePort'
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self._process is not None and self._process.poll() is not None:
                raise RuntimeError('the browser exited before reporting a debugging port. '
                                   f'It said: {self._browser_output() or "nothing"}')
            if port_file.exists():
                first_line = port_file.read_text().splitlines()[:1]
                if first_line and first_line[0].strip().isdigit():
                    return int(first_line[0].strip())
            time.sleep(0.05)
        raise TimeoutError('the browser did not report a debugging port')

    def _find_page(self, port: int, timeout: float = 30.0) -> str:
        """Return the websocket URL of our page.

        An `--app` window opens on about:blank and navigates a moment later, so prefer a target
        that already shows our URL and fall back to any page once we have waited long enough.
        """
        deadline = time.time() + timeout
        accept_any_page_after = time.time() + timeout / 2
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(f'http://127.0.0.1:{port}/json/list', timeout=2) as response:
                    targets = json.load(response)
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
                time.sleep(0.1)
                continue
            pages = [t for t in targets if t.get('type') == 'page' and t.get('webSocketDebuggerUrl')]
            for target in pages:
                if str(target.get('url', '')).startswith(self.url):
                    return str(target['webSocketDebuggerUrl'])
            if pages and time.time() > accept_any_page_after:
                return str(pages[0]['webSocketDebuggerUrl'])  # still navigating; attach anyway
            time.sleep(0.1)
        raise TimeoutError('the browser did not open a page we could attach to')

    def _attach(self, port: int) -> None:
        threading.Thread(target=self._handle_events, daemon=True).start()
        self._protocol = _DevToolsProtocol(self._find_page(port))
        self._protocol_ready.set()
        self._protocol.on_event = lambda method, params: self._events.put_nowait((method, params))
        self._protocol.send('Page.enable')
        self._protocol.send('Runtime.enable')
        try:
            result = self._protocol.send('Browser.getWindowForTarget')
            self._window_id = result['windowId']
            self._bounds = result['bounds']
        except Exception:
            log.debug('could not resolve the browser window; geometry will be approximate')
        if self.title:
            self._apply_title()
        if self._position != (None, None):
            self.move(self._position[0] or 0, self._position[1] or 0)
        # We attach after launching, so the page may already have loaded, in which case
        # Page.loadEventFired never arrives and anything waiting for `loaded` would wait forever.
        if self._is_showing_app() and self.evaluate_js('document.readyState') == 'complete':
            self._synthetic_load_time = time.time()
            self._fire_loaded()

    def _watch(self) -> None:
        """Poll geometry until the browser window goes away, then report it closed."""
        while self._process is not None and self._process.poll() is None:
            self._poll_bounds()
            time.sleep(0.25)
        self._events.put_nowait(('__stop__', {}))
        if self._protocol is not None:
            self._protocol.close()
        self._remove_profile()
        self.events.closed.fire()

    def _terminate_browser(self, timeout: float = 5.0) -> None:
        """Stop the browser and wait for it to exit.

        Waiting matters: a browser that is still running rewrites its profile directory as it
        shuts down, so deleting the directory first only makes it reappear a moment later.
        """
        if self._process is None or self._process.poll() is not None:
            return
        self._process.terminate()
        with suppress(subprocess.TimeoutExpired):
            self._process.wait(timeout=timeout)
        if self._process.poll() is None:
            self._process.kill()
            with suppress(subprocess.TimeoutExpired):
                self._process.wait(timeout=timeout)

    def _browser_output(self) -> str:
        """The last of whatever the browser wrote to stderr, for diagnosing a failed launch."""
        if self._log_file is None:
            return ''
        with suppress(OSError, ValueError):
            self._log_file.seek(0)
            lines = self._log_file.read().decode(errors='replace').strip().splitlines()
            return ' | '.join(lines[-3:])
        return ''

    def _remove_profile(self) -> None:
        """Delete the throwaway browser profile; it is only useful while the window lives.

        Best effort: NiceGUI's native mode also removes fallback profiles from the parent process,
        where app shutdown is observable.
        """
        if self._profile_dir is not None:
            shutil.rmtree(self._profile_dir, ignore_errors=True)
            self._profile_dir = None

    # -- events ------------------------------------------------------------------------------

    def _handle_events(self) -> None:
        """Handle DevTools events off the reader thread, so a handler may itself issue commands."""
        while True:
            method, _ = self._events.get()
            if method == '__stop__':
                return
            try:
                if method == 'Page.loadEventFired':
                    self._on_load()
                elif method == 'Page.frameResized':
                    self._poll_bounds()
            except Exception:
                log.exception(f'error handling DevTools event {method}')

    def _on_load(self) -> None:
        if time.time() - self._synthetic_load_time < 1.0:
            return  # already reported when attaching
        if not self._is_showing_app():
            return  # an --app window loads about:blank first, which is not the page we serve
        self._fire_loaded()

    def _fire_loaded(self) -> None:
        """Apply the title and report the page as loaded."""
        if self.title:
            self._apply_title()
        self.events.loaded.fire()

    def _is_showing_app(self) -> bool:
        location = self.evaluate_js('location.href')
        return isinstance(location, str) and location.startswith(self.url)

    def _apply_title(self) -> None:
        # `--app` takes the window title from the page, so set it explicitly to match pywebview.
        # Note that this is observable to the app's own JavaScript, unlike a real window title.
        self.evaluate_js(f'document.title = {json.dumps(self.title)};')

    def _poll_bounds(self, max_age: float = 0.05) -> None:
        """Refresh the cached window bounds, unless they were read a moment ago.

        native_mode answers get_size() and get_position() by reading x, y, width and height in
        turn, so without this each of those costs a separate round-trip to the browser.
        """
        if self._protocol is None or self._window_id is None:
            return
        if time.monotonic() - self._bounds_checked_at < max_age:
            return
        self._bounds_checked_at = time.monotonic()
        try:
            bounds = self._protocol.send('Browser.getWindowBounds', {'windowId': self._window_id})['bounds']
        except Exception:
            return
        previous, self._bounds = self._bounds, bounds
        if (bounds.get('width'), bounds.get('height')) != (previous.get('width'), previous.get('height')):
            self.events.resized.fire(bounds.get('width', 0), bounds.get('height', 0))
        if (bounds.get('left'), bounds.get('top')) != (previous.get('left'), previous.get('top')):
            self.events.moved.fire(bounds.get('left', 0), bounds.get('top', 0))
        if bounds.get('windowState') != previous.get('windowState'):
            slot = {'minimized': self.events.minimized,
                    'maximized': self.events.maximized,
                    'normal': self.events.restored}.get(bounds.get('windowState', ''))
            if slot is not None:
                slot.fire()

    # -- the pywebview window API ------------------------------------------------------------

    def _await_protocol(self, timeout: float = 60.0) -> _DevToolsProtocol | None:
        """Wait for the browser connection.

        Callers may arrive before `start()` has attached: NiceGUI launches its window-method
        executor first, and it only forwards a response when the method returns something other
        than None, so returning None early would leave the caller waiting forever.

        Callers that only read geometry must not use this: they have a usable default, and
        blocking would turn a plain attribute read into a minute-long hang.
        """
        self._protocol_ready.wait(timeout)
        return self._protocol

    def evaluate_js(self, script: str, *_args: Any, **_kwargs: Any) -> Any:
        protocol = self._await_protocol()
        if protocol is None:
            return None
        try:
            result = protocol.send('Runtime.evaluate', {
                'expression': script,
                'returnByValue': True,
                'awaitPromise': True,
                'userGesture': True,
            })
        except Exception:
            log.debug(f'could not evaluate JavaScript: {script[:60]}')
            return None
        # NOTE: a None result is not forwarded by native_mode's window-method executor, which
        # only queues a response when the method returns something else, and the requesting side
        # waits without a timeout. So `undefined` results and evaluation errors leave an
        # `await main_window.evaluate_js(...)` pending. This predates the fallback but the
        # fallback reaches it more easily.
        if result.get('exceptionDetails'):
            log.debug(f'JavaScript raised: {result["exceptionDetails"].get("text")}')
            return None
        return result.get('result', {}).get('value')

    def get_current_url(self) -> str:
        # never return None: NiceGUI forwards a window method's result only when it is not None,
        # and the requesting side waits for that response without a timeout
        return self.evaluate_js('location.href') or ''

    def get_cookies(self) -> list:
        _warn_unsupported('window.get_cookies()')
        return []

    def _current_bounds(self) -> dict[str, Any]:
        self._poll_bounds()  # deliberately does not wait for the connection; see _await_protocol
        return self._bounds

    @property
    def x(self) -> int:
        return int(self._current_bounds().get('left', 0))

    @property
    def y(self) -> int:
        return int(self._current_bounds().get('top', 0))

    @property
    def width(self) -> int:
        return int(self._current_bounds().get('width', self._initial_size[0]))

    @property
    def height(self) -> int:
        return int(self._current_bounds().get('height', self._initial_size[1]))

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value
        if self._protocol is not None:  # deliberately does not wait; setting a title must not block
            self._apply_title()

    @property
    def on_top(self) -> bool:
        return self._on_top

    @on_top.setter
    def on_top(self, value: bool) -> None:
        self._on_top = value
        _warn_unsupported('keeping the window on top')

    def _set_bounds(self, **bounds: Any) -> None:
        protocol = self._await_protocol(timeout=5.0)  # nobody awaits a result, so do not wait long
        if protocol is None or self._window_id is None:
            return
        try:
            protocol.send('Browser.setWindowBounds', {'windowId': self._window_id, 'bounds': bounds})
        except Exception:
            log.debug('could not change the window bounds')

    def resize(self, width: int, height: int,
               fix_point: FixPoint = FixPoint.NORTH | FixPoint.WEST) -> None:  # pylint: disable=unused-argument
        self._set_bounds(windowState='normal', width=int(width), height=int(height))

    def set_window_size(self, width: int, height: int) -> None:
        self.resize(width, height)

    def move(self, x: int, y: int) -> None:
        self._set_bounds(windowState='normal', left=int(x), top=int(y))

    def minimize(self) -> None:
        self._set_bounds(windowState='minimized')

    def maximize(self) -> None:
        self._set_bounds(windowState='maximized')

    def restore(self) -> None:
        self._set_bounds(windowState='normal')

    def toggle_fullscreen(self) -> None:
        is_fullscreen = self._current_bounds().get('windowState') == 'fullscreen'
        self._set_bounds(windowState='normal' if is_fullscreen else 'fullscreen')

    def show(self) -> None:
        self.restore()

    def hide(self) -> None:
        self.minimize()

    def load_url(self, url: str) -> None:
        self.url = url
        if self._protocol is not None:
            self._protocol.send('Page.navigate', {'url': url})

    def set_title(self, title: str) -> None:
        self._title = title
        self._apply_title()

    def destroy(self) -> None:
        if self._protocol is not None:
            with suppress(Exception):
                self._protocol.send('Browser.close', timeout=2)
        self._terminate_browser()
        # _watch() may not get to run: NiceGUI kills the window subprocess once the app shuts down
        self._remove_profile()

    def __getattr__(self, name: str) -> Callable:
        if name not in UNSUPPORTED_METHODS:
            raise AttributeError(name)

        def unsupported(*_args: Any, **_kwargs: Any) -> None:
            _warn_unsupported(f'window.{name}()')
        return unsupported


_windows: list[Window] = []


def create_window(url: str = '', title: str = '', width: int = 800, height: int = 600,
                  fullscreen: bool = False, frameless: bool = False, **kwargs: Any) -> Window:
    """Mirrors ``webview.create_window``."""
    window = Window(url=url, title=title, width=width, height=height,
                    fullscreen=fullscreen, frameless=frameless, **kwargs)
    _windows.append(window)
    return window


def _close_browsers_on_termination() -> None:
    """Close the browser when this subprocess is told to exit.

    NiceGUI terminates the window subprocess without waiting for it to drain its method queue, so
    a queued `destroy` may never run. Without this the browser is left orphaned and keeps
    rewriting its profile directory.
    """
    previous = signal.getsignal(signal.SIGTERM)

    def handle(signum: int, frame: Any) -> None:
        for window in _windows:
            window._terminate_browser(timeout=2.0)  # pylint: disable=protected-access
            window._remove_profile()  # pylint: disable=protected-access
        if callable(previous) and previous not in (signal.SIG_DFL, signal.SIG_IGN):
            previous(signum, frame)
        sys.exit(0)

    with suppress(ValueError):  # only possible on the main thread
        signal.signal(signal.SIGTERM, handle)


def start(*_args: Any, **_kwargs: Any) -> None:
    """Mirrors ``webview.start``: open the window(s) and block until they are closed."""
    browser = find_browser()
    assert browser is not None, 'no browser found; native_mode.activate() should have caught this'
    log.debug(f'using {browser} for native mode')
    _close_browsers_on_termination()
    for name, ignored in [('settings', sorted(settings)), ('start_args', sorted(_kwargs))]:
        if ignored:
            _warn_unsupported(f'app.native.{name} {ignored}')
    for window in _windows:
        window._launch(browser)  # pylint: disable=protected-access
        try:
            window._attach(window._wait_for_debugging_port())  # pylint: disable=protected-access
        except Exception:
            window.destroy()  # do not leave an orphaned browser and profile behind
            window._remove_profile()  # pylint: disable=protected-access
            raise
        window.events.shown.fire()
    watchers = [threading.Thread(target=w._watch) for w in _windows]  # pylint: disable=protected-access
    for watcher in watchers:
        watcher.start()
    for watcher in watchers:
        watcher.join()


def active_window() -> Window | None:
    """Mirrors ``webview.active_window``."""
    return _windows[0] if _windows else None
