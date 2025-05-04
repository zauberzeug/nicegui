import asyncio
import traceback

from multiprocessing import Pipe, Process

from . import core
from .run import SubprocessException

from .run_simple import io_bound, P, R, Callable


def _worker_process(tx):
    while True:
        func, args, kwargs = tx.recv()
        if func is None:
            break

        result, exception = None, None
        try:
            result = func(*args, *kwargs)
        except Exception as e:
            exception = SubprocessException(type(e).__name__,
                                            str(e), traceback.format_exc())
        tx.send((result, exception))


class Worker:
    def __init__(self):
        self.rx, tx = Pipe()
        self.process = Process(target=_worker_process, args=(tx,))
        self.process.start()

    async def run(self, f, *args, **kwargs):
        assert f is not None
        self.rx.send((f, args, kwargs))
        return await io_bound(self.rx.recv)

    def shutdown(self):
        self.rx.send((None, None, None))
        self.process.join()

    def kill(self):
        self.process.kill()
        self.process.join()


class ProcessPool:
    def __init__(self, max_size=0):
        self.max_size = max_size
        self.worker = []
        self.pool = asyncio.Queue()

    async def get_worker(self):
        def max_workers_reached():
            return self.max_size != 0 and len(self.worker) >= self.max_size

        if max_workers_reached():
            return await self.pool.get()

        if self.pool.empty():
            self.worker.append(Worker())
            return self.worker[-1]

        return self.pool.get_nowait()

    async def run(self, f, *args, **kwargs):
        worker = await self.get_worker()
        result, exception = await worker.run(f, *args, **kwargs)
        await self.pool.put(worker)

        if exception is not None:
            raise exception

        return result

    def shutdown(self):
        for w in self.worker:
            w.shutdown()

    def kill(self):
        for w in self.worker:
            w.kill()


_process_pool = None
async def cpu_bound(callback: Callable[P, R],
                    *args: P.args, **kwargs: P.kwargs) -> R:
    """Run a CPU-bound function in a separate process."""
    if core.app.is_stopping:
        # assumption: the user's code no longer cares about this value
        return  # type: ignore

    global _process_pool
    if _process_pool is None:
        _process_pool = ProcessPool()

    return await _process_pool.run(callback, *args, **kwargs)


def shutdown():
    global _process_pool
    if _process_pool is not None:
        _process_pool.shutdown()
        _process_pool = None
