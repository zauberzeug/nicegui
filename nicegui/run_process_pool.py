import asyncio
import os
import traceback

from functools import partial

from multiprocessing import Pipe, Process


class SubprocessException(Exception):
    """A picklable exception to represent exceptions raised in subprocesses."""

    def __init__(self, original_type, original_message, original_traceback) -> None:
        self.original_type = original_type
        self.original_message = original_message
        self.original_traceback = original_traceback
        super().__init__(f'{original_type}: {original_message}')

    def __reduce__(self):
        return (SubprocessException, (self.original_type,
                                      self.original_message,
                                      self.original_traceback))

    def __str__(self):
        return (f'Exception in subprocess:\n'
                f'  Type: {self.original_type}\n'
                f'  Message: {self.original_message}\n'
                f'  {self.original_traceback}')


async def _io_bound(callback, *args, **kwargs):
    """Run an I/O-bound function in a separate thread."""
    loop = asyncio.get_event_loop()
    # first parameter None -> run in default ThreadPoolExecutor
    return await loop.run_in_executor(None, partial(callback, *args, **kwargs))


def _worker_process(tx):
    try:
        while True:
            func, args, kwargs = tx.recv()
            if func is None:
                break

            result, exception = None, None
            try:
                result = func(*args, *kwargs)
            except Exception as e:
                exception = SubprocessException(type(e).__name__,
                                                str(e),
                                                traceback.format_exc())

            tx.send((result, exception))
    except KeyboardInterrupt:
        pass


class _Worker:
    def __init__(self):
        self.rx, tx = Pipe()
        self.process = Process(target=_worker_process, args=(tx,))
        self.process.daemon = True
        self.process.start()

    async def run(self, f, *args, **kwargs):
        assert f is not None

        self.rx.send((f, args, kwargs))
        return await _io_bound(self.rx.recv)

    def shutdown(self, kill=False):
        if not kill:
            self.rx.send((None, None, None))
        else:
            self.process.kill()
        self.process.join()


class AsyncProcessPool:
    def __init__(self, max_size=os.cpu_count()):
        if max_size is None:
            max_size = 1
        if max_size < 1:
                 raise ValueError("max_size must be at least 1")

        self.worker = [_Worker() for _ in range(max_size)]
        self.pool = asyncio.Queue()
        self.futures = set()
        for w in self.worker:
            self.pool.put_nowait(w)

    async def _get_worker(self):
        assert len(self.worker) > 0

        if self.pool.empty():
            return await self.pool.get()

        return self.pool.get_nowait()

    async def run(self, f, *args, **kwargs):
        worker = await self._get_worker()
        assert worker.process.is_alive()

        result, exception = await worker.run(f, *args, **kwargs)

        self.pool.put_nowait(worker)

        if exception is not None:
            raise exception

        return result

    def submit(self, fn, /, *args, **kwargs):
        task = asyncio.create_task(self.run(fn, *args, **kwargs))

        self.futures.add(task)
        task.add_done_callback(self.futures.discard)

        return task

    def shutdown(self, wait=True, *, cancel_futures=False):
        if cancel_futures:
            for f in self.futures:
                f.cancel()

        if not wait:
            raise ValueError("TODO: handle wait=False")

        for w in self.worker:
            w.shutdown(kill=False)

        self.worker.clear()
        self.pool = asyncio.Queue() # reset / clear pool
