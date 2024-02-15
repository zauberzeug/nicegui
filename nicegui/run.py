import asyncio
import sys
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
from typing import Any, Callable

from . import core, helpers

process_pool = ProcessPoolExecutor()
thread_pool = ThreadPoolExecutor()


async def _run(executor: Any, callback: Callable, *args: Any, **kwargs: Any) -> Any:
    """
    Run the given callback function asynchronously using the provided executor.

    Args:
        executor (Any): The executor to use for running the callback function.
        callback (Callable): The callback function to be executed.
        *args (Any): Positional arguments to be passed to the callback function.
        **kwargs (Any): Keyword arguments to be passed to the callback function.

    Returns:
        Any: The result of the callback function.

    Raises:
        RuntimeError: If the callback function cannot be scheduled due to the event loop being shutdown.

    """
    if core.app.is_stopping:
        return
    try:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, partial(callback, *args, **kwargs))
    except RuntimeError as e:
        if 'cannot schedule new futures after shutdown' not in str(e):
            raise
    except asyncio.exceptions.CancelledError:
        pass


async def cpu_bound(callback: Callable, *args: Any, **kwargs: Any) -> Any:
    """Run a CPU-bound function in a separate process.

    This function is used to execute a CPU-bound function in a separate process. It takes a callback function as the first argument,
    followed by any additional positional and keyword arguments that need to be passed to the callback function.

    Parameters:
        callback (Callable): The CPU-bound function to be executed in a separate process.
        *args (Any): Additional positional arguments to be passed to the callback function.
        **kwargs (Any): Additional keyword arguments to be passed to the callback function.

    Returns:
        Any: The result of the CPU-bound function execution.

    Notes:
        - The `cpu_bound` function needs to execute the callback function in a separate process.
        - To achieve this, it transfers the entire state of the callback function to the process using pickle.
        - It is recommended to create static methods or free functions that accept all the necessary data as simple parameters,
          rather than relying on class or UI logic, and return the result instead of modifying class properties or global variables.
    """
    return await _run(process_pool, callback, *args, **kwargs)


async def io_bound(callback: Callable, *args: Any, **kwargs: Any) -> Any:
    """
    Run an I/O-bound function in a separate thread.

    This function is used to execute I/O-bound functions in a separate thread, allowing the main event loop to continue
    processing other tasks. It is particularly useful when dealing with blocking I/O operations, such as network
    requests or file operations.

    Parameters:
        callback (Callable): The I/O-bound function to be executed.
        *args (Any): Positional arguments to be passed to the callback function.
        **kwargs (Any): Keyword arguments to be passed to the callback function.

    Returns:
        Any: The result of the I/O-bound function.

    Note:
        The callback function should be an async function or a function that returns a coroutine object.

    """
    return await _run(thread_pool, callback, *args, **kwargs)


def tear_down() -> None:
    """Kill all processes and threads.

    This function is responsible for terminating all running processes and threads in the application.
    It is designed to be called when the application is being shut down.

    Usage:
        Call this function when you want to gracefully terminate all processes and threads in the application.

    Raises:
        None

    Returns:
        None
    """
    if helpers.is_pytest():
        return
    for p in process_pool._processes.values():  # pylint: disable=protected-access
        p.kill()
    kwargs = {'cancel_futures': True} if sys.version_info >= (3, 9) else {}
    process_pool.shutdown(wait=True, **kwargs)
    thread_pool.shutdown(wait=False, **kwargs)
