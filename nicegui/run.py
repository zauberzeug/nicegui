import asyncio
import logging
import traceback
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from contextlib import suppress
from functools import partial
from pickle import PicklingError
from typing import Any, TypeVar

from typing_extensions import ParamSpec

from . import core, helpers

process_pool: ProcessPoolExecutor | None = None
thread_pool = ThreadPoolExecutor()

P = ParamSpec('P')
R = TypeVar('R')


def setup() -> None:
    """Setup the process pool. (For internal use only.)"""
    global process_pool  # pylint: disable=global-statement # noqa: PLW0603
    try:
        process_pool = ProcessPoolExecutor()
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
    global process_pool  # pylint: disable=global-statement # noqa: PLW0603

    if process_pool is None:
        raise RuntimeError('Process pool not set up.')

    try:
        return await _run(process_pool, safe_callback, callback, *args, **kwargs)
    except PicklingError as e:
        if core.script_mode:
            raise RuntimeError('Unable to run CPU-bound in script mode. Use a `@ui.page` function instead.') from e
        raise e
    except BrokenProcessPool as e:
        try:
            await _run(process_pool, safe_callback, lambda: None)
        except BrokenProcessPool:
            process_pool = ProcessPoolExecutor()
        finally:
            raise e


async def io_bound(callback: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
    """Run an I/O-bound function in a separate thread."""
    return await _run(thread_pool, callback, *args, **kwargs)


def reset() -> None:
    """Reset process and thread pools. (Useful for testing.)"""
    global process_pool, thread_pool  # pylint: disable=global-statement # noqa: PLW0603

    if process_pool is not None:
        with suppress(Exception):
            _kill_processes()
            process_pool.shutdown(wait=False, cancel_futures=True)
        process_pool = None

    with suppress(Exception):
        thread_pool.shutdown(wait=False, cancel_futures=True)
    thread_pool = ThreadPoolExecutor()


def tear_down() -> None:
    """Kill all processes and threads."""
    if helpers.is_pytest():
        return

    if process_pool is not None:
        _kill_processes()
        process_pool.shutdown(wait=True, cancel_futures=True)
    thread_pool.shutdown(wait=False, cancel_futures=True)


def _kill_processes() -> None:
    assert process_pool is not None
    assert process_pool._processes is not None  # pylint: disable=protected-access
    for p in process_pool._processes.values():  # pylint: disable=protected-access
        p.kill()
