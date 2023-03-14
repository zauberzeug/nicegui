import multiprocessing
import os
import signal
import socket
import tempfile
import time
from threading import Thread

import webview

shutdown = multiprocessing.Event()


def open_window(event, fullscreen) -> None:
    window = webview.create_window('NiceGUI', url='http://localhost:8080', fullscreen=fullscreen)
    window.events.closing += event.set  # signal that the program should be closed to the main process
    webview.start(storage_path=tempfile.mkdtemp())


def check_shutdown() -> None:
    while True:
        if shutdown.is_set():
            os.kill(os.getpgid(os.getpid()), signal.SIGTERM)
        time.sleep(0.1)


def activate(fullscreen: bool = False) -> None:
    multiprocessing.Process(target=open_window, args=(shutdown, fullscreen), daemon=False).start()
    Thread(target=check_shutdown, daemon=True).start()


def find_open_port(start_port=8000, end_port=9000):
    for port in range(start_port, end_port+1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            pass
    raise OSError('No open port found')
