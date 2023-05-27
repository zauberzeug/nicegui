import _thread
import logging
import multiprocessing as mp
import queue
import socket
import sys
import tempfile
import time
import warnings
from threading import Event, Thread

from . import globals, helpers, native

try:
    with warnings.catch_warnings():
        # webview depends on bottle which uses the deprecated CGI function (https://github.com/bottlepy/bottle/issues/1403)
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        import webview
except ModuleNotFoundError:
    pass


def open_window(
    host: str, port: int, title: str, width: int, height: int, fullscreen: bool,
    method_queue: mp.Queue, response_queue: mp.Queue,
) -> None:
    while not helpers.is_port_open(host, port):
        time.sleep(0.1)

    window_kwargs = dict(url=f'http://{host}:{port}', title=title, width=width, height=height, fullscreen=fullscreen)
    window_kwargs.update(globals.app.native.window_args)

    try:
        window = webview.create_window(**window_kwargs)
        closing = Event()
        window.events.closing += lambda: closing.set()
        start_window_method_executor(window, method_queue, response_queue, closing)
        webview.start(storage_path=tempfile.mkdtemp(), **globals.app.native.start_args)
    except NameError:
        logging.error('Native mode is not supported in this configuration. Please install pywebview to use it.')
        sys.exit(1)


def start_window_method_executor(
        window: webview.Window, method_queue: mp.Queue, response_queue: mp.Queue, closing: Event
) -> None:
    def execute(attr, args, kwargs):
        response = attr(*args, **kwargs)
        if response is not None or 'dialog' in attr.__name__:
            response_queue.put(response)

    def window_method_executor():
        pending_executions = []
        while not closing.is_set():
            try:
                method, args, kwargs = method_queue.get(block=False)
                if method == 'signal_server_shutdown':
                    if pending_executions:
                        logging.warning('shutdown is possibly blocked by opened dialogs like a file picker')
                        while pending_executions:
                            pending_executions.pop().join()
                    continue
                if method == 'is_always_on_top':
                    response_queue.put(window.on_top)
                    continue
                if method == 'set_always_on_top':
                    window.on_top = args[0]
                    continue
                if method == 'get_position':
                    response_queue.put((int(window.x), int(window.y)))
                    continue
                if method == 'get_size':
                    response_queue.put((int(window.width), int(window.height)))
                    continue
                attr = getattr(window, method)
                if callable(attr):
                    pending_executions.append(Thread(target=execute, args=(attr, args, kwargs)))
                    pending_executions[-1].start()
                else:
                    logging.error(f'window.{method} is not callable')
            except queue.Empty:
                time.sleep(0.01)
            except Exception:
                logging.exception(f'error in window.{method}')

    Thread(target=window_method_executor).start()


def activate(host: str, port: int, title: str, width: int, height: int, fullscreen: bool) -> None:
    def check_shutdown() -> None:
        while process.is_alive():
            time.sleep(0.1)
        globals.server.should_exit = True
        while globals.state != globals.State.STOPPED:
            time.sleep(0.1)
        _thread.interrupt_main()

    mp.freeze_support()
    process = mp.Process(
        target=open_window,
        args=(host, port, title, width, height, fullscreen, native.method_queue, native.response_queue),
        daemon=False
    )
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
