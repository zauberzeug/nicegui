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

from temp_webview.window import _open_window


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
