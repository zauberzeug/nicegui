from __future__ import annotations

import functools
import hashlib
import inspect
import os
import socket
import struct
import sys
import threading
import time
import webbrowser
from collections.abc import Callable
from inspect import Parameter, signature
from pathlib import Path
from typing import TYPE_CHECKING, Any, Union

from .context import context
from .logging import log

if TYPE_CHECKING:
    from .element import Element

_shown_warnings: set[str] = set()

if sys.version_info < (3, 13):
    from asyncio import iscoroutinefunction
else:
    from inspect import iscoroutinefunction


class WEAK_DEFAULT:
    pass


def weaken_defaults(original_func):
    """Create a generic wrapper that detects if certain parameters have a WEAK_DEFAULT type hint.

    If that is the case, we pass WEAK_DEFAULT for that parameter if the user does not provide a value.
    This way, the default value shown in the IDE is just for decorative purposes.
    """
    weak_args = set()
    for name, annotation in original_func.__annotations__.items():
        if getattr(annotation, '__origin__', None) is Union:
            for arg in annotation.__args__:
                if arg is WEAK_DEFAULT:
                    weak_args.add(name)

    sentinels = {param_name: object() for param_name in weak_args}

    sig = inspect.signature(original_func)

    new_params = [param.replace(default=sentinels[param.name]) if param.name in sentinels else param
                  for param in sig.parameters.values()]

    new_sig = sig.replace(parameters=new_params)

    @functools.wraps(original_func)
    def wrapper(*args, **kwargs):
        bound_args = new_sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        return original_func(**{
            param_name: (WEAK_DEFAULT
                         if param_name in sentinels and value is sentinels[param_name]
                         else value)
            for param_name, value in bound_args.arguments.items()
        })

    wrapper.__signature__ = new_sig

    return wrapper


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


def is_coroutine_function(obj: Any) -> bool:
    """Check if the object is a coroutine function.

    This function is needed because functools.partial is not a coroutine function, but its func attribute is.
    Note: It will return false for coroutine objects.
    """
    while isinstance(obj, functools.partial):
        obj = obj.func
    return iscoroutinefunction(obj)


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


def schedule_browser(protocol: str, host: str, port: int) -> tuple[threading.Thread, threading.Event]:
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

    def in_thread(protocol: str, host: str, port: int) -> None:
        while not is_port_open(host, port):
            if cancel.is_set():
                return
            time.sleep(0.1)
        webbrowser.open(f'{protocol}://{host}:{port}/')

    host = host if host != '0.0.0.0' else '127.0.0.1'
    thread = threading.Thread(target=in_thread, args=(protocol, host, port), daemon=True)
    thread.start()
    return thread, cancel


def kebab_to_camel_case(string: str) -> str:
    """Convert a kebab-case string to camelCase."""
    return ''.join(word.capitalize() if i else word for i, word in enumerate(string.split('-')))


def event_type_to_camel_case(string: str) -> str:
    """Convert an event type string to camelCase."""
    return '.'.join(kebab_to_camel_case(part) if part != '-' else part for part in string.split('.'))


def require_top_level_layout(element: Element) -> None:
    """Check if the element is a top level layout element."""
    parent = context.slot.parent
    if parent != parent.client.content:
        raise RuntimeError(
            f'Found top level layout element "{element.__class__.__name__}" inside element "{parent.__class__.__name__}". '
            'Top level layout elements can not be nested but must be direct children of the page content.',
        )
