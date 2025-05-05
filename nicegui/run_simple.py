import traceback

from multiprocessing import Pipe, Process

from . import core
from .run import SubprocessException, io_bound, Callable, P, R

async def cpu_bound(callback: Callable[P, R],
                    *args: P.args, **kwargs: P.kwargs) -> R:
    """Run a CPU-bound function in a separate process."""
    if core.app.is_stopping:
        # assumption: the user's code no longer cares about this value
        return  # type: ignore

    rx, tx = Pipe()

    p = Process(target=_cpu_bound_wrapper, args=(tx, callback, args, kwargs))
    p.start()

    (result, exception) = await io_bound(rx.recv)
    if exception is not None:
        raise exception

    return result


def _cpu_bound_wrapper(tx, callback, args, kwargs):
    result, exception = None, None
    try:
        result = callback(*args, **kwargs)
    except Exception as e:
        exception = SubprocessException(type(e).__name__, str(e), traceback.format_exc())
    tx.send((result, exception))
