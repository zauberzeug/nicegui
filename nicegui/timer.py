import asyncio
import time
from typing import Awaitable, Callable, ClassVar, Optional, Set

from . import background_tasks, core, logging
from .awaitable_response import AwaitableResponse


class Timer:
    tasks: ClassVar[Set[asyncio.Task]] = set()

    def __init__(self, interval: float, handler: Callable) -> None:
        self.handler = handler
        self.interval = interval
        self._task: Optional[asyncio.Task] = None

    def start(self) -> None:
        """Start the timer."""
        if self.running:
            return
        if core.app.is_started or core.app.is_starting:
            self._task = background_tasks.create(self._repeat())
            self.tasks.add(self._task)
        elif self.start not in core.app._startup_handlers:  # pylint: disable=protected-access
            print('add to startup handlers')
            core.app.on_startup(self.start)

    async def _repeat(self) -> None:
        await asyncio.sleep(self.interval)  # TODO: sleep immediately?
        while True:
            start = time.time()
            try:
                if core.app.is_stopping:
                    logging.log.info('%s must be stopped', self.handler)
                    break
                await self._invoke_callback()
                dt = time.time() - start
            except (asyncio.CancelledError, GeneratorExit):
                return
            except Exception:
                dt = time.time() - start
                logging.log.exception('error in "%s"', self.handler.__qualname__)
                if self.interval == 0 and dt < 0.1:
                    delay = 0.1 - dt
                    logging.log.warning(
                        f'"{self.handler.__qualname__}" would be called to frequently ' +
                        f'because it only took {dt*1000:.0f} ms; ' +
                        f'delaying this step for {delay*1000:.0f} ms')
                    await asyncio.sleep(delay)
            try:
                await asyncio.sleep(self.interval - dt)
            except (asyncio.CancelledError, GeneratorExit):
                return

    async def _invoke_callback(self) -> None:
        try:
            assert self.handler is not None
            result = self.handler()
            if isinstance(result, Awaitable) and not isinstance(result, AwaitableResponse):
                await result
        except Exception as e:
            core.app.handle_exception(e)

    def stop(self) -> None:
        """Stop the timer."""
        if not self._task:
            return

        if not self._task.done():
            self._task.cancel()

        self.tasks.remove(self._task)
        self._task = None

    @property
    def running(self) -> bool:
        """Whether the timer is running."""
        return self._task is not None and not self._task.done()

    @running.setter
    def running(self, value: bool) -> None:
        if value:
            self.start()
        else:
            self.stop()

    @staticmethod
    def stop_all() -> None:
        """Stop all timers."""
        for timer in Timer.tasks:
            timer.cancel()
