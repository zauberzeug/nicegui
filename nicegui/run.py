import asyncio
import logging
import multiprocessing
import signal
import traceback
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from contextlib import suppress
from functools import partial
from multiprocessing.context import BaseContext
from pickle import PicklingError
from typing import Any, TypeVar

from typing_extensions import ParamSpec

from . import core, helpers

process_pool: ProcessPoolExecutor | None = None
thread_pool = ThreadPoolExecutor()

# Start method for the run.cpu_bound process pool (tri-state, see #6117):
#   None    -> inherit the global multiprocessing default (byte-for-byte today's behavior); a
#              one-time heads-up is logged on first use if that resolves to plain 'fork' (Linux).
#   'spawn' -> opt in to spawn, silent. Workers start from a fresh import: they do NOT inherit
#              process state (module globals, caches, preloaded objects), and callables + args must
#              be picklable -- already the contract on macOS/Windows. Also avoids the fork deadlock.
#   'fork'  -> opt out, keep fork, silent. You own the fork-safety risk.
# TODO(4.0): flip the None default to 'spawn' (keeping the explicit 'fork' opt-out). See #6117.
process_pool_start_method: str | None = None

# Always-spawn context, also shared with native.py's window subprocess (#1841). This is the context
# used when process_pool_start_method == 'spawn'; it is independent of the global default.
SPAWN_CONTEXT = multiprocessing.get_context('spawn')

# Resolved once in setup() so the live pool, the heads-up warning and the BrokenProcessPool restart
# all agree, even if process_pool_start_method is mutated after startup.
_pool_context: BaseContext | None = None
_pool_uses_implicit_fork = False

P = ParamSpec('P')
R = TypeVar('R')


def _resolve_cpu_bound_context() -> BaseContext:
    """Resolve the multiprocessing context for the cpu_bound pool from `process_pool_start_method`."""
    if process_pool_start_method is None:
        return multiprocessing.get_context()  # global default -> byte-for-byte today's behavior
    if process_pool_start_method == 'spawn':
        return SPAWN_CONTEXT
    if process_pool_start_method == 'fork':
        try:
            return multiprocessing.get_context('fork')
        except ValueError as e:  # e.g. Windows, where 'fork' does not exist
            raise ValueError("run.process_pool_start_method='fork' is not available on this platform "
                             "(e.g. Windows); use 'spawn' or None instead.") from e
    raise ValueError(f'Invalid run.process_pool_start_method {process_pool_start_method!r}; '
                     "expected None, 'spawn' or 'fork'.")


def _warn_if_implicit_fork() -> None:
    """Warn once if the live pool fell back to plain fork because the start method was never chosen."""
    if _pool_uses_implicit_fork:
        helpers.warn_once(
            "run.cpu_bound is using the 'fork' start method (the platform default on Linux/Docker). "
            'fork is unsafe in a threaded process and its workers inherit process state (module globals, '
            'caches, preloaded objects) that spawn workers do not, so switching can change behavior. '
            "NiceGUI 4.0 will default to 'spawn'. Set nicegui.run.process_pool_start_method to 'spawn' to "
            "opt in now (recommended) or to 'fork' to keep fork and silence this heads-up; "
            'the setting must be applied before the app starts up (i.e. before ui.run()). '
            'See https://github.com/zauberzeug/nicegui/pull/6117'
        )


def setup() -> None:
    """Setup the process pool. (For internal use only.)"""
    global process_pool, _pool_context, _pool_uses_implicit_fork  # pylint: disable=global-statement # noqa: PLW0603
    _pool_context = _resolve_cpu_bound_context()
    _pool_uses_implicit_fork = process_pool_start_method is None and _pool_context.get_start_method() == 'fork'
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
    (``'spawn'``, ``'fork'`` or ``None`` to inherit the platform default) before the app starts up.

    Returns ``None`` (instead of the callback's result) when the call is cancelled or the app is shutting down.
    This ``None`` return is an interim shape: NiceGUI 4.0 will instead raise ``CancelledError`` in these cases,
    so ``if result is None: ...`` checks should be treated as temporary.
    """
    global process_pool  # pylint: disable=global-statement # noqa: PLW0603

    if process_pool is None:
        raise RuntimeError('Process pool not set up.')

    _warn_if_implicit_fork()

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
