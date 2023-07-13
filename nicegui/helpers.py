import asyncio
import functools
import hashlib
import inspect
import mimetypes
import socket
import sys
import threading
import time
import webbrowser
from contextlib import nullcontext
from pathlib import Path
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Generator, List, Optional, Tuple, Union

import netifaces
from fastapi import Request
from fastapi.responses import StreamingResponse
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from . import background_tasks, globals
from .storage import RequestTrackingMiddleware

if TYPE_CHECKING:
    from .client import Client

mimetypes.init()

KWONLY_SLOTS = {'kw_only': True, 'slots': True} if sys.version_info >= (3, 10) else {}


def is_pytest() -> bool:
    """Check if the code is running in pytest."""
    return 'pytest' in sys.modules


def is_coroutine_function(object: Any) -> bool:
    """Check if the object is a coroutine function.

    This function is needed because functools.partial is not a coroutine function, but its func attribute is.
    Note: It will return false for coroutine objects.
    """
    while isinstance(object, functools.partial):
        object = object.func
    return asyncio.iscoroutinefunction(object)


def is_file(path: Optional[Union[str, Path]]) -> bool:
    """Check if the path is a file that exists."""
    if not path:
        return False
    elif isinstance(path, str) and path.strip().startswith('data:'):
        return False  # NOTE: avoid passing data URLs to Path
    try:
        return Path(path).is_file()
    except OSError:
        return False


def hash_file_path(path: Path) -> str:
    return hashlib.sha256(str(path).encode()).hexdigest()[:32]


def safe_invoke(func: Union[Callable[..., Any], Awaitable], client: Optional['Client'] = None) -> None:
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


def schedule_browser(host: str, port: int) -> Tuple[threading.Thread, threading.Event]:
    """Wait non-blockingly for the port to be open, then start a webbrowser.

    This function launches a thread in order to be non-blocking.
    This thread then uses `is_port_open` to check when the port opens.
    When connectivity is confirmed, the webbrowser is launched using `webbrowser.open`.

    The thread is created as a daemon thread, in order to not interfere with Ctrl+C.

    If you need to stop this thread, you can do this by setting the Event, that gets returned.
    The thread will stop with the next loop without opening the browser.

    :return: A tuple consisting of the actual thread object and an event for stopping the thread.
    """
    cancel = threading.Event()

    def in_thread(host: str, port: int) -> None:
        while not is_port_open(host, port):
            if cancel.is_set():
                return
            time.sleep(0.1)
        webbrowser.open(f'http://{host}:{port}/')

    host = host if host != '0.0.0.0' else '127.0.0.1'
    thread = threading.Thread(target=in_thread, args=(host, port), daemon=True)
    thread.start()
    return thread, cancel


def set_storage_secret(storage_secret: Optional[str] = None) -> None:
    """Set storage_secret and add request tracking middleware."""
    if any(m.cls == SessionMiddleware for m in globals.app.user_middleware):
        # NOTE not using "add_middleware" because it would be the wrong order
        globals.app.user_middleware.append(Middleware(RequestTrackingMiddleware))
    elif storage_secret is not None:
        globals.app.add_middleware(RequestTrackingMiddleware)
        globals.app.add_middleware(SessionMiddleware, secret_key=storage_secret)


def get_streaming_response(file: Path, request: Request) -> StreamingResponse:
    file_size = file.stat().st_size
    start = 0
    end = file_size - 1
    range_header = request.headers.get('Range')
    if range_header:
        byte1, byte2 = range_header.split('=')[1].split('-')
        start = int(byte1)
        if byte2:
            end = int(byte2)
    content_length = end - start + 1
    headers = {
        'Content-Range': f'bytes {start}-{end}/{file_size}',
        'Content-Length': str(content_length),
        'Accept-Ranges': 'bytes',
    }

    def content_reader(file: Path, start: int, end: int, chunk_size: int = 8192) -> Generator[bytes, None, None]:
        with open(file, 'rb') as data:
            data.seek(start)
            remaining_bytes = end - start + 1
            while remaining_bytes > 0:
                chunk = data.read(min(chunk_size, remaining_bytes))
                if not chunk:
                    break
                yield chunk
                remaining_bytes -= len(chunk)

    return StreamingResponse(
        content_reader(file, start, end),
        media_type=mimetypes.guess_type(str(file))[0] or 'application/octet-stream',
        headers=headers,
        status_code=206,
    )


def get_all_ips() -> List[str]:
    ips = []
    for interface in netifaces.interfaces():
        try:
            ips.append(netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr'])
        except KeyError:
            pass
    return ips
