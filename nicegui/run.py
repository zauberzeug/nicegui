import asyncio
import logging
import multiprocessing
import multiprocessing.forkserver
import signal
import traceback
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from contextlib import suppress
from functools import partial
from multiprocessing.context import BaseContext
from pickle import PicklingError
from typing import Any, Literal, ParamSpec, TypeVar

from . import core, helpers

process_pool: ProcessPoolExecutor | None = None
thread_pool = ThreadPoolExecutor()

# Start method for the run.cpu_bound process pool (None inherits the global multiprocessing default);
# see the multiprocessing docs for the trade-offs between the methods.
# The default is "spawn", because plain "fork" is unsafe in a threaded process (#6117).
process_pool_start_method: Literal['spawn', 'fork', 'forkserver'] | None = 'spawn'

# Always-spawn context, also shared with native.py's window subprocess (#1841). This is the context
# used when process_pool_start_method == 'spawn'; it is independent of the global default.
SPAWN_CONTEXT = multiprocessing.get_context('spawn')

# Resolved once in setup() so the live pool and the BrokenProcessPool restart
# agree, even if process_pool_start_method is mutated after startup.
_pool_context: BaseContext | None = None

P = ParamSpec('P')
R = TypeVar('R')


def _resolve_cpu_bound_context() -> BaseContext:
    """Resolve the multiprocessing context for the cpu_bound pool from `process_pool_start_method`."""
    if process_pool_start_method is None:
        return multiprocessing.get_context()
    if process_pool_start_method == 'spawn':
        return SPAWN_CONTEXT
    try:
        return multiprocessing.get_context(process_pool_start_method)
    except ValueError as e:  # unknown method, or a method this platform lacks (e.g. "fork" on Windows)
        raise ValueError(f'Invalid run.process_pool_start_method {process_pool_start_method!r}; '
                         f'this platform supports {multiprocessing.get_all_start_methods()}.') from e


def setup() -> None:
    """Setup the process pool. (For internal use only.)"""
    global process_pool, _pool_context  # pylint: disable=global-statement # noqa: PLW0603
    _pool_context = _resolve_cpu_bound_context()
    if _pool_context.get_start_method() == 'forkserver':
        # drop __main__ from the preload so the workers re-import it, where the MainProcess guard catches it,
        # not the daemon (#6166); other (user-configured) preload modules are kept
        fork_server = multiprocessing.forkserver._forkserver  # pylint: disable=protected-access
        preload = fork_server._preload_modules  # type: ignore[attr-defined]  # pylint: disable=protected-access
        _pool_context.set_forkserver_preload([module for module in preload if module != '__main__'])
    try:
        process_pool = ProcessPoolExecutor(mp_context=_pool_context, initializer=_ignore_sigint)
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
        # we do not want to pass the original exception because it might be unpicklable
        raise SubprocessException(type(e).__name__, str(e), traceback.format_exc()) from None


async def _run(executor: Any, callback: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R | None:
    if core.app.is_stopping:
        return None  # DEPRECATED: This is an interim shape. NiceGUI 4.0 will instead raise CancelledError in this case.
    try:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, partial(callback, *args, **kwargs))
    except RuntimeError as e:
        if 'cannot schedule new futures after shutdown' not in str(e):
            raise
    except asyncio.CancelledError:
        pass
    return None  # DEPRECATED: This is an interim shape. NiceGUI 4.0 will instead raise CancelledError in this case.


async def cpu_bound(callback: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R | None:
    """Run a CPU-bound function in a separate process.

    `run.cpu_bound` needs to execute the function in a separate process.
    For this it needs to transfer the whole state of the passed function to the process (which is done with pickle).
    It is encouraged to create static methods (or free functions) which get all the data as simple parameters (eg. no class/ui logic)
    and return the result (instead of writing it in class properties or global variables).

    The pool's multiprocessing start method can be configured via ``run.process_pool_start_method``
    ("spawn" by default, "fork", "forkserver", or ``None`` to inherit the platform default) before the app starts up.

    Returns ``None`` (instead of the callback's result) when the call is cancelled or the app is shutting down.
    This ``None`` return is an interim shape: NiceGUI 4.0 will instead raise ``CancelledError`` in these cases,
    so ``if result is None: ...`` checks should be treated as temporary.
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
            process_pool = ProcessPoolExecutor(mp_context=_pool_context, initializer=_ignore_sigint)
        finally:
            raise e


async def io_bound(callback: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R | None:
    """Run an I/O-bound function in a separate thread.

    Returns ``None`` (instead of the callback's result) when the call is cancelled or the app is shutting down.
    This ``None`` return is an interim shape: NiceGUI 4.0 will instead raise ``CancelledError`` in these cases,
    so ``if result is None: ...`` checks should be treated as temporary.
    """
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


def _ignore_sigint() -> None:
    """Ignore SIGINT in worker processes so only the parent handles Ctrl-C (see #6025)."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def _kill_processes() -> None:
    assert process_pool is not None
    assert process_pool._processes is not None  # pylint: disable=protected-access
    for p in process_pool._processes.values():  # pylint: disable=protected-access
        p.kill()
