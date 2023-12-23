import asyncio
import sys
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
from typing import Any, Callable

from . import context, core, helpers, storage

process_pool = ProcessPoolExecutor()
thread_pool = ThreadPoolExecutor()


async def _run(executor: Any, callback: Callable, *args: Any, **kwargs: Any) -> Any:
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
    """Run a CPU-bound function in a separate process."""
    return await _run(process_pool, callback, *args, **kwargs)


async def io_bound(callback: Callable, *args: Any, **kwargs: Any) -> Any:
    """Run an I/O-bound function in a separate thread."""

    slot_stack = context.get_slot_stack()
    request = storage.request_contextvar.get()

    def with_context():
        storage.request_contextvar.set(request)
        if slot_stack:
            parent_slot = slot_stack[-1]
            with parent_slot:
                return callback(*args, **kwargs)
        else:
            return callback(*args, **kwargs)

    return await _run(thread_pool, with_context)


def tear_down() -> None:
    """Kill all processes and threads."""
    if helpers.is_pytest():
        return
    for p in process_pool._processes.values():  # pylint: disable=protected-access
        p.kill()
    kwargs = {'cancel_futures': True} if sys.version_info >= (3, 9) else {}
    process_pool.shutdown(wait=True, **kwargs)
    thread_pool.shutdown(wait=False, **kwargs)
