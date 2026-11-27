import asyncio
import itertools
import multiprocessing
import multiprocessing.forkserver
import signal
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from contextlib import suppress
from functools import partial
from multiprocessing.context import BaseContext
from pickle import PicklingError
from typing import Any, Literal, ParamSpec, TypeVar

from _nicegui_worker import SubprocessException, safe_callback  # noqa: F401  # pylint: disable=unused-import

from . import core, helpers
from .logging import log

process_pool: ProcessPoolExecutor | None = None
thread_pool = ThreadPoolExecutor()

# Start method for the run.cpu_bound process pool (None inherits the global multiprocessing default);
# see the multiprocessing docs for the trade-offs between the methods.
# The default is "spawn", because plain "fork" is unsafe in a threaded process (#6117).
process_pool_start_method: Literal['spawn', 'fork', 'forkserver'] | None = 'spawn'

# Always-spawn context, also used by native.py's window subprocess (#1841).
# The cpu_bound pool derives its own context from it when process_pool_start_method == 'spawn'.
# It is independent of the global default.
SPAWN_CONTEXT = multiprocessing.get_context('spawn')

# Resolved once in setup() so the live pool and the BrokenProcessPool restart
# agree, even if process_pool_start_method is mutated after startup.
_pool_context: BaseContext | None = None

P = ParamSpec('P')
R = TypeVar('R')


def _resolve_cpu_bound_context() -> BaseContext:
    """Resolve the multiprocessing context for the cpu_bound pool from ``process_pool_start_method``."""
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
    """Set up the process pool. (For internal use only.)"""
    global process_pool, _pool_context  # pylint: disable=global-statement # noqa: PLW0603
    _pool_context = _resolve_cpu_bound_context()
    if _pool_context.get_start_method() == 'forkserver':
        # drop __main__ from the preload so the workers re-import it, where the MainProcess guard catches it,
        # not the daemon (#6166); other (user-configured) preload modules are kept
        fork_server = multiprocessing.forkserver._forkserver  # pylint: disable=protected-access
        preload = fork_server._preload_modules  # type: ignore[attr-defined]  # pylint: disable=protected-access
        _pool_context.set_forkserver_preload([module for module in preload if module != '__main__'])
    _pool_context = _with_worker_names(_pool_context)
    try:
        process_pool = _create_process_pool()
    except NotImplementedError:
        log.warning('Failed to initialize ProcessPoolExecutor')


def _with_worker_names(context: BaseContext) -> BaseContext:
    """Create a context of the same type whose processes are named "NiceGUIWorker-<n>".

    A spawned worker gets its name before it re-imports the main module,
    so the main module can check the name to skip its NiceGUI code (#5684).
    Overriding the context's ``Process`` factory keeps the process object itself a plain one,
    which the worker unpickles without importing NiceGUI (unlike a ``Process`` subclass defined here).
    """
    numbers = itertools.count(1)

    class WorkerContext(type(context)):  # type: ignore[misc]
        def Process(self, *args, **kwargs):
            """Create a process named "NiceGUIWorker-<n>"."""
            kwargs['name'] = f'NiceGUIWorker-{next(numbers)}'
            return super().Process(*args, **kwargs)
    return WorkerContext()


def _create_process_pool() -> ProcessPoolExecutor:
    # ignore SIGINT in worker processes so only the parent handles Ctrl-C (#6025);
    # signal.signal is passed directly, because unpickling a NiceGUI function would import NiceGUI in the worker (#5684)
    return ProcessPoolExecutor(mp_context=_pool_context, initializer=signal.signal, initargs=(signal.SIGINT, signal.SIG_IGN))


async def _run(executor: Any, callback: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
    try:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, partial(callback, *args, **kwargs))
    except RuntimeError as e:
        if 'cannot schedule new futures after shutdown' not in str(e):
            raise
        raise asyncio.CancelledError('The app has shut down.') from e


async def cpu_bound(callback: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
    """Run a CPU-bound function in a separate process.

    ``run.cpu_bound`` needs to execute the function in a separate process.
    For this it needs to transfer the whole state of the passed function to the process (which is done with pickle).
    It is encouraged to create static methods (or free functions) which get all the data as simple parameters (e.g. no class/ui logic)
    and return the result (instead of writing it in class properties or global variables).

    The pool's multiprocessing start method can be configured via ``run.process_pool_start_method``
    ("spawn" by default, "fork", "forkserver", or ``None`` to inherit the platform default) before the app starts up.

    Raises ``asyncio.CancelledError`` when the call is cancelled or the app has shut down
    (*updated in version 4.0.0*: before it returned ``None`` in these cases and while the app was shutting down).
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
            process_pool = _create_process_pool()
        finally:
            raise e


async def io_bound(callback: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
    """Run an I/O-bound function in a separate thread.

    Raises ``asyncio.CancelledError`` when the call is cancelled or the app has shut down
    (*updated in version 4.0.0*: before it returned ``None`` in these cases and while the app was shutting down).
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


def _kill_processes() -> None:
    assert process_pool is not None
    assert process_pool._processes is not None  # pylint: disable=protected-access
    for p in process_pool._processes.values():  # pylint: disable=protected-access
        p.kill()
