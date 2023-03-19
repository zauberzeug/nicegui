import multiprocessing
import os
import signal
import socket
import tempfile
import time
import warnings
from threading import Thread

with warnings.catch_warnings():
    # webview depends on bottle which uses the deprecated CGI function (https://github.com/bottlepy/bottle/issues/1403)
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    import webview

shutdown = multiprocessing.Event()


def open_window(url: str, title: str, width: int, height: int, fullscreen: bool, shutdown: multiprocessing.Event) -> None:
    window = webview.create_window(title, url=url, width=width, height=height, fullscreen=fullscreen)
    window.events.closing += shutdown.set  # signal to the main process that the program should be closed
    webview.start(storage_path=tempfile.mkdtemp())


def check_shutdown() -> None:
    while True:
        if shutdown.is_set():
            os.kill(os.getpgid(os.getpid()), signal.SIGTERM)
        time.sleep(0.1)


def activate(url: str, title: str, width: int, height: int, fullscreen: bool) -> None:
    args = url, title, width, height, fullscreen, shutdown
    multiprocessing.Process(target=open_window, args=args, daemon=False).start()
    Thread(target=check_shutdown, daemon=True).start()


def find_open_port(start_port: int = 8000, end_port: int = 8999) -> int:
    '''Reliably find an open port in a given range.

    This function will actually try to open the port to ensure no firewall blocks it.
    This is better than, e.g., passing port=0 to uvicorn.
    '''
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            pass
    raise OSError('No open port found')
