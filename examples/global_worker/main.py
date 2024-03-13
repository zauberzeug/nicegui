#!/usr/bin/env python3
import asyncio
import time
from multiprocessing import Manager
from queue import Empty, Queue
from typing import Callable, Generator

from nicegui import app, background_tasks, run, ui


class Worker:

    def __init__(self) -> None:
        self._queue: Queue
        self.progress: float = 0.0
        self.is_running: bool = False

        app.on_startup(self._create_queue)

    async def run(self, func: Callable[..., Generator[float, None, None]]) -> None:
        background_tasks.create(run.cpu_bound(self._run_generator, func, self._queue))
        background_tasks.create(self._consume_queue())

    @staticmethod
    def _run_generator(func: Callable[..., Generator[float, None, None]], queue: Queue) -> None:
        for progress in func():
            queue.put({'progress': progress})
        queue.put({'progress': 1.0})

    def _create_queue(self) -> None:
        self._queue = Manager().Queue()

    async def _consume_queue(self) -> None:
        self.is_running = True
        self.progress = 0.0
        while self.progress < 1.0:
            try:
                msg = self._queue.get_nowait()
            except Empty:
                await asyncio.sleep(0.1)
                continue
            self.progress = msg['progress']
        self.is_running = False


def heavy_computation() -> Generator[float, None, None]:
    n = 50
    for i in range(n):
        time.sleep(0.1)
        yield i / n


worker = Worker()


@ui.page('/')
def main_page():
    ui.button('compute', on_click=lambda: worker.run(heavy_computation))
    ui.linear_progress().props('instant-feedback') \
        .bind_value_from(worker, 'progress') \
        .bind_visibility_from(worker, 'is_running')


ui.run()
