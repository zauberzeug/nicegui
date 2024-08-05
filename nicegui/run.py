import asyncio
import sys
import traceback
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
from typing import Any, Callable, TypeVar

from typing_extensions import ParamSpec

from . import core, helpers

process_pool = ProcessPoolExecutor()
thread_pool = ThreadPoolExecutor()

P = ParamSpec('P')
R = TypeVar('R')


class SubprocessException(Exception):
    """A picklable exception to represent exceptions raised in subprocesses."""

    def __init__(self, original_type, original_message, original_traceback) -> None:
        self.original_type = original_type
        self.original_message = original_message
        self.original_traceback = original_traceback
        super().__init__(f'{original_type}: {original_message}')

    def __reduce__(self):
        return (SubprocessException, (self.original_type, self.original_message, self.original_traceback))

    def __str__(self):
        return (f'Exception in subprocess:\n'
                f'  Type: {self.original_type}\n'
                f'  Message: {self.original_message}\n'
                f'  {self.original_traceback}')


def safe_callback(callback: Callable, *args, **kwargs) -> Any:
    """Run a callback; catch and wrap any exceptions that might occur."""
    try:
        return callback(*args, **kwargs)
    except Exception as e:
        # NOTE: we do not want to pass the original exception because it might be unpicklable
        raise SubprocessException(type(e).__name__, str(e), traceback.format_exc()) from None


async def _run(executor: Any, callback: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
    if core.app.is_stopping:
        return  # type: ignore  # the assumption is that the user's code no longer cares about this value
    try:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, partial(callback, *args, **kwargs))
    except RuntimeError as e:
        if 'cannot schedule new futures after shutdown' not in str(e):
            raise
    except asyncio.CancelledError:
        pass
    return  # type: ignore  # the assumption is that the user's code no longer cares about this value


async def cpu_bound(callback: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
    """Run a CPU-bound function in a separate process.

    `run.cpu_bound` needs to execute the function in a separate process.
    For this it needs to transfer the whole state of the passed function to the process (which is done with pickle).
    It is encouraged to create static methods (or free functions) which get all the data as simple parameters (eg. no class/ui logic)
    and return the result (instead of writing it in class properties or global variables).
    """
    return await _run(process_pool, safe_callback, callback, *args, **kwargs)


async def io_bound(callback: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
    """Run an I/O-bound function in a separate thread."""
    return await _run(thread_pool, callback, *args, **kwargs)


def tear_down() -> None:
    """Kill all processes and threads."""
    if helpers.is_pytest():
        return
    for p in process_pool._processes.values():  # pylint: disable=protected-access
        p.kill()
    kwargs = {'cancel_futures': True} if sys.version_info >= (3, 9) else {}
    process_pool.shutdown(wait=True, **kwargs)
    thread_pool.shutdown(wait=False, **kwargs)
