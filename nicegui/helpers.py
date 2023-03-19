import asyncio
import functools
import inspect
import socket
import threading
import time
import webbrowser
from contextlib import nullcontext
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional, Union

from . import background_tasks, globals

if TYPE_CHECKING:
    from .client import Client


def is_coroutine(object: Any) -> bool:
    while isinstance(object, functools.partial):
        object = object.func
    return asyncio.iscoroutinefunction(object)


def safe_invoke(func: Union[Callable, Awaitable], client: Optional['Client'] = None) -> None:
    try:
        if isinstance(func, Awaitable):
            async def func_with_client():
                with client or nullcontext():
                    await func
            background_tasks.create(func_with_client())
        else:
            with client or nullcontext():
                result = func(client) if len(inspect.signature(func).parameters) == 1 and client is not None else func()
            if isinstance(result, Awaitable):
                async def result_with_client():
                    with client or nullcontext():
                        await result
                background_tasks.create(result_with_client())
    except Exception as e:
        globals.handle_exception(e)


def port_open_tcp(host: str, port: int) -> bool:
    # Check if the port is open by checking if a TCP connection can be established.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except ConnectionRefusedError:
        return False
    else:
        return True
    finally:
        sock.close()


def schedule_browser(host: str, port: int) -> None:
    # This function has to be non blocking. Therefore, we'll launch a thread, s.th.
    # the main thread can proceed with the actual startup.
    # The thread will be launched as a daemon, s.th. it doesn't interfere with Ctrl+C.
    def thread(host: str, port: int) -> None:
        while not port_open_tcp(host, port):
            time.sleep(0.1)
        webbrowser.open(f'http://{host}:{port}/')

    host = host if host != "0.0.0.0" else "127.0.0.1"
    threading.Thread(target=thread, args=(host, port), daemon=True).start()
