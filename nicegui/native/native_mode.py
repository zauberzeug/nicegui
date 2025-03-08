from __future__ import annotations

import _thread
import multiprocessing as mp
import socket
import sys
import time
from threading import Thread

from nicegui_webview.window import open_window, register

from .. import core, optional_features
from ..logging import log
from ..server import Server
from . import native


def activate(host: str, port: int, title: str, width: int, height: int, fullscreen: bool, frameless: bool) -> None:
    """Activate native mode."""
    def check_shutdown() -> None:
        while process.is_alive():
            time.sleep(0.1)
        Server.instance.should_exit = True
        while not core.app.is_stopped:
            time.sleep(0.1)
        _thread.interrupt_main()

    webview_registered = register()
    if webview_registered:
        optional_features.register('webview')

    if not optional_features.has('webview'):
        log.error('Native mode is not supported in this configuration.\n'
                  'Please run "pip install pywebview" to use it.')
        sys.exit(1)

    mp.freeze_support()
    args = (host, port, title, width, height, fullscreen, frameless, native.method_queue, native.response_queue,
            core.app.native.window_args, core.app.native.settings, core.app.native.start_args)
    process = mp.Process(target=open_window, args=args, daemon=True)
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
