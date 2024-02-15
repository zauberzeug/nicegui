import asyncio
import functools
import hashlib
import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path
from typing import Any, Optional, Tuple, Union


def is_pytest() -> bool:
    """
    Check if the code is running in pytest.

    Returns:
        bool: True if running in pytest, False otherwise.

    Examples:
        >>> is_pytest()
        False
    """
    return 'pytest' in sys.modules


def is_coroutine_function(obj: Any) -> bool:
    """
    Check if the object is a coroutine function.

    This function checks if the given object is a coroutine function. It is useful when dealing with objects that may be
    wrapped in `functools.partial` and need to determine if the underlying function is a coroutine function.

    Parameters:
        obj (Any): The object to be checked.

    Returns:
        bool: True if the object is a coroutine function, False otherwise.

    Notes:
        - This function will return False for coroutine objects.
        - If the object is a `functools.partial` object, it will unwrap it until it reaches the underlying function.

    Example:
        >>> async def my_coroutine():
        ...     pass
        ...
        >>> def my_function():
        ...     pass
        ...
        >>> is_coroutine_function(my_coroutine)
        True
        >>> is_coroutine_function(my_function)
        False
    """
    while isinstance(obj, functools.partial):
        obj = obj.func
    return asyncio.iscoroutinefunction(obj)


def is_file(path: Optional[Union[str, Path]]) -> bool:
    """
    Check if the path is a file that exists.

    Args:
        path (Optional[Union[str, Path]]): The path to check.

    Returns:
        bool: True if the path is a file that exists, False otherwise.

    Raises:
        None

    Notes:
        - If the path is None or empty, it will return False.
        - If the path starts with 'data:', it will return False to avoid passing data URLs to Path.
        - If an OSError occurs while checking the path, it will return False.
    """
    if not path:
        return False
    if isinstance(path, str) and path.strip().startswith('data:'):
        return False  # NOTE: avoid passing data URLs to Path
    try:
        return Path(path).is_file()
    except OSError:
        return False


def hash_file_path(path: Path) -> str:
    """
    Hashes the given file path using SHA256 algorithm.

    Args:
        path (Path): The path of the file to be hashed.

    Returns:
        str: The hashed value of the file path.

    Raises:
        None
    """
    return hashlib.sha256(path.as_posix().encode()).hexdigest()[:32]


def is_port_open(host: str, port: int) -> bool:
    """
    Check if the port is open by attempting to establish a TCP connection.

    Args:
        host (str): The hostname or IP address of the target.
        port (int): The port number to check.

    Returns:
        bool: True if the port is open, False otherwise.

    Raises:
        None
    """
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
    """
    Wait non-blockingly for the port to be open, then start a web browser.

    This function launches a thread in order to be non-blocking.
    The thread continuously checks if the specified port is open using `is_port_open` function.
    Once the port is open, it launches a web browser to open the specified URL.

    The thread is created as a daemon thread to ensure it does not interfere with Ctrl+C.

    If you need to stop this thread, you can do so by setting the returned Event object.
    The thread will stop on the next loop iteration without opening the browser.

    - host: The host address to connect to. If '0.0.0.0', it will be replaced with '127.0.0.1'.
    - port: The port number to check for connectivity.

    :return: A tuple consisting of the thread object and an event for stopping the thread.
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


def kebab_to_camel_case(string: str) -> str:
    """
    Convert a kebab-case string to camelCase.

    Args:
        string (str): The kebab-case string to be converted.

    Returns:
        str: The converted camelCase string.

    Examples:
        >>> kebab_to_camel_case("hello-world")
        'helloWorld'
        >>> kebab_to_camel_case("my-name-is-john")
        'myNameIsJohn'
    """
    return ''.join(word.capitalize() if i else word for i, word in enumerate(string.split('-')))
