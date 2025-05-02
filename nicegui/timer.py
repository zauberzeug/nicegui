import asyncio
import time
from contextlib import nullcontext
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, ContextManager, Optional, cast

from typing_extensions import Self

from . import background_tasks, core
from .awaitable_response import AwaitableResponse
from .binding import BindableProperty
from .dataclasses import KWONLY_SLOTS
from .events import EventArguments, Handler, handle_event


@dataclass(**KWONLY_SLOTS)
class BaseTimerIntervalChangeEventArguments(EventArguments):
    sender: 'Timer'
    interval: float


@dataclass(**KWONLY_SLOTS)
class BaseTimerActiveChangeEventArguments(EventArguments):
    sender: 'Timer'
    active: bool


class AlreadyRanOnceError(Exception):
    """Exception raised when the timer has already run once, so as to stop the outer while loop in _run_in_loop."""


class Timer:
    active = BindableProperty(
        on_change=lambda sender, active: cast(Self, sender)._handle_active_change(active))  # pylint: disable=protected-access
    interval = BindableProperty(
        on_change=lambda sender, interval: cast(Self, sender)._handle_interval_change(interval))  # pylint: disable=protected-access

    def __init__(self,
                 interval: float,
                 callback: Callable[..., Any], *,
                 active: bool = True,
                 once: bool = False,
                 immediate: bool = True,
                 on_active_changed: Optional[Handler[BaseTimerActiveChangeEventArguments]] = None,
                 on_interval_changed: Optional[Handler[BaseTimerIntervalChangeEventArguments]] = None,
                 ) -> None:
        """Timer

        One major drive behind the creation of NiceGUI was the necessity to have a simple approach to update the interface in regular intervals,
        for example to show a graph with incoming measurements.
        A timer will execute a callback repeatedly with a given interval.

        :param interval: the interval in which the timer is called (can be changed during runtime)
        :param callback: function or coroutine to execute when interval elapses
        :param active: whether the callback should be executed or not (can be changed during runtime)
        :param once: whether the callback is only executed once after a delay specified by `interval` (default: `False`, can be changed during runtime)
        :param immediate: whether the callback should be executed immediately (default: `True`, ignored if `once` is `True`, *added in version 2.9.0*)
        :param on_active_changed: callback which is invoked when the active state is changed (default: `None`)
        :param on_interval_changed: callback which is invoked when the interval is changed (default: `None`)
        """
        super().__init__()
        self.interval = interval
        self.callback: Optional[Callable[..., Any]] = callback
        self.active = active
        self._is_canceled = False
        self.once = once
        self._immediate = immediate if not once else False
        self._should_abort_sleep = asyncio.Event()
        self._skip_callback_once_for_reset = False
        self._base_active_changed_handlers = [on_active_changed] if on_active_changed else []
        self._base_interval_changed_handlers = [on_interval_changed] if on_interval_changed else []

        coroutine = self._run_in_loop
        if core.app.is_started:
            background_tasks.create(coroutine(), name=str(callback))
        else:
            core.app.on_startup(coroutine)

    def _handle_active_change(self, active: bool) -> None:
        for handler in self._base_active_changed_handlers:
            handle_event(handler, BaseTimerActiveChangeEventArguments(sender=self, active=active))

    def _handle_interval_change(self, interval: float) -> None:
        for handler in self._base_interval_changed_handlers:
            handle_event(handler, BaseTimerIntervalChangeEventArguments(sender=self, interval=interval))

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

    def trigger(self) -> None:
        """Abort sleep to reset the remaining sleep time to the interval, triggering the callback immediately in doing so."""
        assert not self._is_canceled, 'Cannot trigger a canceled timer'
        self._should_abort_sleep.set()

    def reset(self) -> None:
        """Abort sleep to reset the remaining sleep time to the interval, but without triggering the callback."""
        assert not self._is_canceled, 'Cannot reset a canceled timer'
        self._skip_callback_once_for_reset = True
        self.trigger()

    def on_active_changed(self, callback: Handler[BaseTimerActiveChangeEventArguments]) -> Self:
        """Set a callback which is invoked when the active state is changed."""
        self._base_active_changed_handlers.append(callback)
        return self

    def on_interval_changed(self, callback: Handler[BaseTimerIntervalChangeEventArguments]) -> Self:
        """Set a callback which is invoked when the interval is changed."""
        self._base_interval_changed_handlers.append(callback)
        return self

    async def _sleep_with_abort(self, seconds: float) -> None:
        """Sleep for a given number of seconds, but allow to abort the sleep."""
        if seconds <= 0:
            return
        try:
            await asyncio.wait_for(self._should_abort_sleep.wait(), timeout=seconds)
            self._should_abort_sleep.clear()
        except asyncio.TimeoutError:
            pass

    async def _run_in_loop(self) -> None:
        try:
            if not self._immediate:
                await self._sleep_with_abort(self.interval)
            if not await self._can_start():
                return
            with self._get_context():
                while not self._should_stop():
                    try:
                        start = time.time()
                        if self.active:
                            await self._invoke_callback()
                        dt = time.time() - start
                        await self._sleep_with_abort(self.interval - dt)
                    except AlreadyRanOnceError:
                        break
                    except asyncio.CancelledError:
                        break
                    except Exception as e:
                        core.app.handle_exception(e)
                        await self._sleep_with_abort(self.interval)
        finally:
            self._cleanup()

    async def _invoke_callback(self) -> None:
        try:
            if self._skip_callback_once_for_reset:
                self._skip_callback_once_for_reset = False
                return
            assert self.callback is not None
            result = self.callback()
            if isinstance(result, Awaitable) and not isinstance(result, AwaitableResponse):
                await result
        except Exception as e:
            core.app.handle_exception(e)
        finally:
            if self.once:
                raise AlreadyRanOnceError('Timer has already run once and is set to once=True')

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
