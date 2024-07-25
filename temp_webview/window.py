from __future__ import annotations

import logging
import multiprocessing as mp
import queue
import socket
import tempfile
import time
import warnings
from threading import Event, Thread
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Tuple

import webview

log: logging.Logger = logging.getLogger('nicegui')



def register() -> bool:
    try:
        with warnings.catch_warnings():
            # webview depends on bottle which uses the deprecated CGI function (https://github.com/bottlepy/bottle/issues/1403)
            warnings.filterwarnings('ignore', category=DeprecationWarning)
            import webview
        return True
        #optional_features.register('webview')
    except ModuleNotFoundError:
        return False

def open_window(
    host: str, port: int, title: str, width: int, height: int, fullscreen: bool, frameless: bool,
    method_queue: mp.Queue, response_queue: mp.Queue, window_args, settings, start_args,
) -> None:
    while not is_port_open(host, port):
        time.sleep(0.1)

    window_kwargs = {
        'url': f'http://{host}:{port}',
        'title': title,
        'width': width,
        'height': height,
        'fullscreen': fullscreen,
        'frameless': frameless,
        **window_args,
    }
    webview.settings.update(**settings)
    window = webview.create_window(**window_kwargs)
    closed = Event()
    window.events.closed += closed.set
    _start_window_method_executor(window, method_queue, response_queue, closed)
    webview.start(storage_path=tempfile.mkdtemp(), **start_args)


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

def is_port_open(host: str, port: int) -> bool:
    """Check if the port is open by checking if a TCP connection can be established."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except (ConnectionRefusedError, TimeoutError):
        return False
    except Exception:
        return False
    else:
        return True
    finally:
        sock.close()