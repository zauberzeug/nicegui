from contextlib import nullcontext
from inspect import signature
from typing import Any, Callable, ContextManager, Optional, Union

from typing_extensions import Self

from ..client import Client
from ..element import Element
from ..events import Handler, TimerActiveChangeEventArguments, TimerIntervalChangeEventArguments, handle_event
from ..logging import log
from ..timer import BaseTimerActiveChangeEventArguments, BaseTimerIntervalChangeEventArguments
from ..timer import Timer as BaseTimer


class Timer(BaseTimer, Element, component='timer.js'):

    def __init__(self,
                 interval: float,
                 callback: Callable[..., Any], *,
                 active: bool = True,
                 once: bool = False,
                 immediate: bool = True,
                 on_active_changed: Optional[Handler[TimerActiveChangeEventArguments]] = None,
                 on_interval_changed: Optional[Handler[TimerIntervalChangeEventArguments]] = None,
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
        super().__init__(interval=interval, callback=callback, active=active, once=once, immediate=immediate)

        self._active_changed_handlers = [on_active_changed] if on_active_changed else []
        self._interval_changed_handlers = [on_interval_changed] if on_interval_changed else []

    def _handle_active_change(self, active: bool) -> None:
        super()._handle_active_change(active)
        for handler in self._active_changed_handlers:
            handle_event(handler, TimerActiveChangeEventArguments(sender=self, client=self.client, active=active))

    def _handle_interval_change(self, interval: float) -> None:
        super()._handle_interval_change(interval)
        for handler in self._interval_changed_handlers:
            handle_event(handler, TimerIntervalChangeEventArguments(sender=self, client=self.client, interval=interval))

    def on_active_changed(self, callback: Union[Handler[TimerActiveChangeEventArguments], Handler[BaseTimerActiveChangeEventArguments]]) -> Self:
        """Set a callback which is invoked when the active state is changed."""
        if any(p.annotation is BaseTimerActiveChangeEventArguments for p in signature(callback).parameters.values()):
            super().on_active_changed(callback)
        else:
            self._active_changed_handlers.append(callback)
        return self

    def on_interval_changed(self, callback: Union[Handler[TimerIntervalChangeEventArguments], Handler[BaseTimerIntervalChangeEventArguments]]) -> Self:
        """Set a callback which is invoked when the interval is changed."""
        if any(p.annotation is BaseTimerIntervalChangeEventArguments for p in signature(callback).parameters.values()):
            super().on_interval_changed(callback)
        else:
            self._interval_changed_handlers.append(callback)
        return self

    def _get_context(self) -> ContextManager:
        return self.parent_slot or nullcontext()

    async def _can_start(self) -> bool:
        """Wait for the client connection before the timer callback can be allowed to manipulate the state.

        See https://github.com/zauberzeug/nicegui/issues/206 for details.
        Returns True if the client is connected, False if the client is not connected and the timer should be cancelled.
        """
        if self.client.shared:
            return True

        # ignore served pages which do not reconnect to backend (e.g. monitoring requests, scrapers etc.)
        TIMEOUT = 60.0
        try:
            await self.client.connected(timeout=TIMEOUT)
            return True
        except TimeoutError:
            log.error(f'Timer cancelled because client is not connected after {TIMEOUT} seconds')
            return False

    def _should_stop(self) -> bool:
        return (
            self.is_deleted or
            self.client.id not in Client.instances or
            super()._should_stop()
        )

    def _cleanup(self) -> None:
        super()._cleanup()
        if not self._deleted:
            assert self.parent_slot
            self.parent_slot.parent.remove(self)

    def set_visibility(self, visible: bool) -> None:
        raise NotImplementedError('Use `activate()`, `deactivate()` or `cancel()`. See #3670 for more information.')
