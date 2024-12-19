import asyncio
import time
from contextlib import nullcontext
from typing import Any, Awaitable, Callable, ContextManager, Optional

from . import background_tasks, core
from .awaitable_response import AwaitableResponse
from .binding import BindableProperty


class Timer:
    active = BindableProperty()
    interval = BindableProperty()

    def __init__(self,
                 interval: float,
                 callback: Callable[..., Any], *,
                 active: bool = True,
                 once: bool = False,
                 immediate: bool = True,
                 ) -> None:
        """Timer

        One major drive behind the creation of NiceGUI was the necessity to have a simple approach to update the interface in regular intervals,
        for example to show a graph with incoming measurements.
        A timer will execute a callback repeatedly with a given interval.

        :param interval: the interval in which the timer is called (can be changed during runtime)
        :param callback: function or coroutine to execute when interval elapses
        :param active: whether the callback should be executed or not (can be changed during runtime)
        :param once: whether the callback is only executed once after a delay specified by `interval` (default: `False`)
        :param immediate: whether the callback should be executed immediately (default: `True`, ignored if `once` is `True`)
        """
        super().__init__()
        self.interval = interval
        self.callback: Optional[Callable[..., Any]] = callback
        self.active = active
        self._is_canceled = False
        self._immediate = immediate

        coroutine = self._run_once if once else self._run_in_loop
        if core.app.is_started:
            background_tasks.create(coroutine(), name=str(callback))
        else:
            core.app.on_startup(coroutine)

    def _get_context(self) -> ContextManager:
        return nullcontext()

    def activate(self) -> None:
        """Activate the timer."""
        assert not self._is_canceled, 'Cannot activate a canceled timer'
        self.active = True

    def deactivate(self) -> None:
        """Deactivate the timer."""
        self.active = False

    def cancel(self) -> None:
        """Cancel the timer."""
        self._is_canceled = True

    async def _run_once(self) -> None:
        try:
            if not await self._can_start():
                return
            with self._get_context():
                await asyncio.sleep(self.interval)
                if self.active and not self._should_stop():
                    await self._invoke_callback()
        finally:
            self._cleanup()

    async def _run_in_loop(self) -> None:
        try:
            if not self._immediate:
                await asyncio.sleep(self.interval)
            if not await self._can_start():
                return
            with self._get_context():
                while not self._should_stop():
                    try:
                        start = time.time()
                        if self.active:
                            await self._invoke_callback()
                        dt = time.time() - start
                        await asyncio.sleep(self.interval - dt)
                    except asyncio.CancelledError:
                        break
                    except Exception as e:
                        core.app.handle_exception(e)
                        await asyncio.sleep(self.interval)
        finally:
            self._cleanup()

    async def _invoke_callback(self) -> None:
        try:
            assert self.callback is not None
            result = self.callback()
            if isinstance(result, Awaitable) and not isinstance(result, AwaitableResponse):
                await result
        except Exception as e:
            core.app.handle_exception(e)

    async def _can_start(self) -> bool:
        return True

    def _should_stop(self) -> bool:
        return (
            self._is_canceled or
            core.app.is_stopping or
            core.app.is_stopped
        )

    def _cleanup(self) -> None:
        self.callback = None
