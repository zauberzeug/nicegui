import asyncio
import time
from collections.abc import Awaitable, Callable
from contextlib import AbstractContextManager, nullcontext
from typing import Any

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
        :param immediate: whether the callback should be executed immediately (default: `True`, ignored if `once` is `True`, *added in version 2.9.0*)
        """
        super().__init__()
        self.interval = interval
        self.callback: Callable[..., Any] | None = callback
        self.active = active
        self._is_canceled = False
        self._immediate = immediate
        self._current_invocation: asyncio.Task | None = None

        coroutine = self._run_once if once else self._run_in_loop
        if core.is_script_mode_preflight():
            return
        if core.app.is_started:
            background_tasks.create(coroutine(), name=str(callback))
        else:
            core.app.on_startup(coroutine)

    def _get_context(self) -> AbstractContextManager:
        return nullcontext()

    def activate(self) -> None:
        """Activate the timer."""
        assert not self._is_canceled, 'Cannot activate a canceled timer'
        self.active = True

    def deactivate(self) -> None:
        """Deactivate the timer."""
        self.active = False

    def cancel(self, *, with_current_invocation: bool = False) -> None:
        """Cancel the timer.

        :param with_current_invocation: whether to cancel the currently invoked task of the callback (*added in version 2.23.0*)
        """
        self._is_canceled = True
        if with_current_invocation and self._current_invocation is not None:
            self._current_invocation.cancel()

    async def _run_once(self) -> None:
        try:
            if not await self._can_start():
                return
            with self._get_context():
                await asyncio.sleep(self.interval)
                if self.active and not self._should_stop():
                    self._current_invocation = asyncio.create_task(self._invoke_callback())
                    await self._current_invocation
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
                            self._current_invocation = asyncio.create_task(self._invoke_callback())
                            await self._current_invocation
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
        with self._get_context():
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
