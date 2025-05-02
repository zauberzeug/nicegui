import traceback

from multiprocessing import Pipe, Process
from typing import Callable
from typing_extensions import ParamSpec, TypeVar

from . import core
from .run import SubprocessException, _run

P = ParamSpec('P')
R = TypeVar('R')


async def io_bound(callback: Callable[P, R],
                   *args: P.args, **kwargs: P.kwargs) -> R:
    """Run an I/O-bound function in a separate thread."""
    # use the default executor because it must be a ThreadPoolExecutor
    return await _run(None, callback, *args, **kwargs)


async def cpu_bound(callback: Callable[P, R],
                    *args: P.args, **kwargs: P.kwargs) -> R:
    """Run a CPU-bound function in a separate process."""
    if core.app.is_stopping:
        # assumption: the user's code no longer cares about this value
        return  # type: ignore

    rx, tx = Pipe()

    p = Process(target=_cpu_bound_wrapper, args=(tx, callback, args, kwargs))
    p.start()

    res = await io_bound(rx.recv)

    if isinstance(res, SubprocessException):
        raise res

    return res


def _cpu_bound_wrapper(tx, callback, args, kwargs):
    try:
        res = callback(*args, **kwargs)
    except Exception as e:
        res = SubprocessException(type(e).__name__, str(e), traceback.format_exc())
    tx.send(res)
