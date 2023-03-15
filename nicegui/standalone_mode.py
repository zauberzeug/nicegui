import multiprocessing
import os
import signal
import socket
import tempfile
import time
from threading import Thread

import webview

shutdown = multiprocessing.Event()


def open_window(url: str, title: str, width: int, height: int, fullscreen: bool, shutdown: multiprocessing.Event) -> None:
    window = webview.create_window(title, url=url, width=width, height=height, fullscreen=fullscreen)
    window.events.closing += shutdown.set  # signal that the program should be closed to the main process
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
