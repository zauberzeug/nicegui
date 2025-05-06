import asyncio
import logging
import sys
import traceback
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, Executor
from functools import partial
from typing import Any, Callable, Optional, TypeVar

from typing_extensions import ParamSpec

from . import core, helpers

ProcessPoolExecutorType: type = ProcessPoolExecutor
process_pool: Optional[Executor] = None
thread_pool = ThreadPoolExecutor()

P = ParamSpec('P')
R = TypeVar('R')


def set_cpu_bound_executor_type(executor_type: type):
    """Set concurrent.futures.Executor compliant type for cpu_bound execution

        Note: unfortunately this function will (very likely) be called before
              all functions that are supposed to be called through the executor
              are defined. As a result we can not instantiate the executor in
              this function. If we would, the forked worker processes would not
              be able to call these functions, because they are not defined yet
              and thus don't exist in processes that are forked NOW....
              Therefor this uncommon approach.
    """
    # makes no sense to call this function after ui.run which calls setup, right???
    assert process_pool is None
    assert type(executor_type) is type

    global ProcessPoolExecutorType # pylint: disable=global-statement # noqa: PLW0603
    ProcessPoolExecutorType = executor_type


def setup() -> None:
    """Setup the process pool. (For internal use only.)"""
    global process_pool  # pylint: disable=global-statement # noqa: PLW0603
    try:
        process_pool = ProcessPoolExecutorType()
    except NotImplementedError:
        logging.warning('Failed to initialize ProcessPoolExecutor')


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
    if process_pool is None:
        raise RuntimeError('Process pool not set up.')

    return await _run(process_pool, safe_callback, callback, *args, **kwargs)


async def io_bound(callback: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
    """Run an I/O-bound function in a separate thread."""
    return await _run(thread_pool, callback, *args, **kwargs)


def tear_down() -> None:
    """Kill all processes and threads."""
    if helpers.is_pytest():
        return

    kwargs = {'cancel_futures': True} if sys.version_info >= (3, 9) else {}
    if process_pool is not None:
        if isinstance(process_pool, ProcessPoolExecutor):
            for p in process_pool._processes.values():  # pylint: disable=protected-access
                p.kill()
        process_pool.shutdown(wait=True, **kwargs)
    thread_pool.shutdown(wait=False, **kwargs)
