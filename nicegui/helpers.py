from __future__ import annotations

import asyncio
import hashlib
import os
import socket
import struct
import threading
import time
import webbrowser
from abc import abstractmethod
from collections.abc import Awaitable, Callable
from contextlib import AbstractContextManager
from inspect import Parameter, signature
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeGuard, TypeVar

from .context import context
from .logging import log

if TYPE_CHECKING:
    from .element import Element

_shown_warnings: set[str] = set()
_T = TypeVar('_T')


class SelfManagedAwaitable(Awaitable):
    """Marker base for awaitables that manage their own execution."""

    @abstractmethod
    def __await__(self):
        """Return an iterator used to await the object."""


def warn_once(message: str, *, stack_info: bool = False) -> None:
    """Print a warning message only once."""
    if message not in _shown_warnings:
        log.warning(message, stack_info=stack_info)
        _shown_warnings.add(message)


def is_pytest() -> bool:
    """Check if the code is running in pytest."""
    return 'PYTEST_CURRENT_TEST' in os.environ


def is_user_simulation() -> bool:
    """Check if the code is running in with user simulation (see https://nicegui.io/documentation/user)."""
    return 'NICEGUI_USER_SIMULATION' in os.environ


def expects_arguments(func: Callable) -> bool:
    """Check if the function expects non-variable arguments without a default value."""
    return any(p.default is Parameter.empty and
               p.kind is not Parameter.VAR_POSITIONAL and
               p.kind is not Parameter.VAR_KEYWORD
               for p in signature(func).parameters.values())


def is_file(path: str | Path | None) -> bool:
    """Check if the path is a file that exists."""
    if not path:
        return False
    if isinstance(path, str) and path.strip().startswith('data:'):
        return False  # NOTE: avoid passing data URLs to Path
    try:
        return Path(path).is_file()
    except OSError:
        return False


def hash_file_path(path: Path, *, max_time: float | None = None) -> str:
    """Hash the given path based on its string representation and optionally the last modification time of given files."""
    hasher = hashlib.sha256(path.as_posix().encode())
    if max_time is not None:
        hasher.update(struct.pack('!d', max_time))
    return hasher.hexdigest()[:32]


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


def schedule_browser(protocol: str, host: str, port: int, path: str) -> tuple[threading.Thread, threading.Event]:
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

    def in_thread(protocol: str, host: str, port: int, path: str) -> None:
        while not is_port_open(host, port):
            if cancel.is_set():
                return
            time.sleep(0.1)
        webbrowser.open(f'{protocol}://{host}:{port}/{path.lstrip("/")}')

    host = host if host != '0.0.0.0' else '127.0.0.1'
    thread = threading.Thread(target=in_thread, args=(protocol, host, port, path), daemon=True)
    thread.start()
    return thread, cancel


def kebab_to_camel_case(string: str) -> str:
    """Convert a kebab-case string to camelCase."""
    return ''.join(word.capitalize() if i else word for i, word in enumerate(string.split('-')))


def event_type_to_camel_case(string: str) -> str:
    """Convert an event type string to camelCase."""
    return '.'.join(kebab_to_camel_case(part) if part != '-' else part for part in string.split('.'))


def should_await(result: Any) -> TypeGuard[Awaitable[Any]]:
    """Determine if a result should be awaited.

    Returns ``True`` for awaitables that are not already managed
    (i.e. not a ``SelfManagedAwaitable`` or an ``asyncio.Task``).

    Note: We want to await an awaitable result even if the handler is not an async function (like a lambda statement).
    """

    return isinstance(result, Awaitable) and not isinstance(result, (SelfManagedAwaitable, asyncio.Task))


async def await_with_context(awaitable: Awaitable[_T], ctx: AbstractContextManager) -> _T:
    """Await an awaitable within a context manager."""
    with ctx:
        return await awaitable


def normalize_lifecycle_handler(
    handler: Callable[..., Any] | Awaitable[Any],
    registration: str, *,
    reject: bool = True,
) -> Callable[..., Any]:
    """Normalize lifecycle handler registration for callable-only and deprecated-awaitable paths."""
    if callable(handler):
        return handler
    if not isinstance(handler, Awaitable):
        raise TypeError(f'{registration} expects a synchronous or asynchronous function.')

    if reject:
        raise TypeError(f'{registration} expects a synchronous or asynchronous function, not an awaitable object. '
                        'Pass the function itself instead of calling it.',)

    # DEPRECATED: remove direct awaitable lifecycle registrations in NiceGUI 4.0
    def wrapped_handler() -> Awaitable[Any]:
        return handler
    warn_once(f'Passing an awaitable directly to {registration} is deprecated and will be removed in NiceGUI 4.0. '
              'Pass a synchronous or asynchronous function instead.')
    wrapped_handler.__name__ = f'deprecated {registration} awaitable'
    return wrapped_handler


def require_top_level_layout(element: Element) -> None:
    """Check if the element is a top level layout element."""
    parent = context.slot.parent
    if parent != parent.client.content:
        raise RuntimeError(
            f'Found top level layout element "{element.__class__.__name__}" inside element "{parent.__class__.__name__}". '
            'Top level layout elements can not be nested but must be direct children of the page content.',
        )
