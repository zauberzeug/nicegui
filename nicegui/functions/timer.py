import asyncio
import time
from typing import Any, Callable, Optional

from .. import background_tasks, globals
from ..binding import BindableProperty
from ..helpers import is_coroutine_function
from ..slot import Slot


class Timer:
    active = BindableProperty()
    interval = BindableProperty()

    def __init__(self,
                 interval: float,
                 callback: Callable[..., Any], *,
                 active: bool = True,
                 once: bool = False,
                 ) -> None:
        """Timer

        One major drive behind the creation of NiceGUI was the necessity to have a simple approach to update the interface in regular intervals,
        for example to show a graph with incoming measurements.
        A timer will execute a callback repeatedly with a given interval.

        :param interval: the interval in which the timer is called (can be changed during runtime)
        :param callback: function or coroutine to execute when interval elapses
        :param active: whether the callback should be executed or not (can be changed during runtime)
        :param once: whether the callback is only executed once after a delay specified by `interval` (default: `False`)
        """
        self.interval = interval
        self.callback: Optional[Callable[..., Any]] = callback
        self.active = active
        self.slot: Optional[Slot] = globals.get_slot()

        coroutine = self._run_once if once else self._run_in_loop
        if globals.state == globals.State.STARTED:
            background_tasks.create(coroutine(), name=str(callback))
        else:
            globals.app.on_startup(coroutine)

    def activate(self) -> None:
        """Activate the timer."""
        self.active = True

    def deactivate(self) -> None:
        """Deactivate the timer."""
        self.active = False

    async def _run_once(self) -> None:
        try:
            if not await self._connected():
                return
            assert self.slot is not None
            with self.slot:
                await asyncio.sleep(self.interval)
                if globals.state not in {globals.State.STOPPING, globals.State.STOPPED}:
                    await self._invoke_callback()
        finally:
            self._cleanup()

    async def _run_in_loop(self) -> None:
        try:
            if not await self._connected():
                return
            assert self.slot is not None
            with self.slot:
                while True:
                    if self.slot.parent.client.id not in globals.clients:
                        break
                    if globals.state in {globals.State.STOPPING, globals.State.STOPPED}:
                        break
                    try:
                        start = time.time()
                        if self.active:
                            await self._invoke_callback()
                        dt = time.time() - start
                        await asyncio.sleep(self.interval - dt)
                    except asyncio.CancelledError:
                        break
                    except Exception as e:
                        globals.handle_exception(e)
                        await asyncio.sleep(self.interval)
        finally:
            self._cleanup()

    async def _invoke_callback(self) -> None:
        try:
            assert self.callback is not None
            result = self.callback()
            if is_coroutine_function(self.callback):
                await result
        except Exception as e:
            globals.handle_exception(e)

    async def _connected(self, timeout: float = 60.0) -> bool:
        """Wait for the client connection before the timer callback can be allowed to manipulate the state.

        See https://github.com/zauberzeug/nicegui/issues/206 for details.
        Returns True if the client is connected, False if the client is not connected and the timer should be cancelled.
        """
        assert self.slot is not None
        if self.slot.parent.client.shared:
            return True
        else:
            # ignore served pages which do not reconnect to backend (eg. monitoring requests, scrapers etc.)
            try:
                await self.slot.parent.client.connected(timeout=timeout)
                return True
            except TimeoutError:
                globals.log.error(f'Timer cancelled because client is not connected after {timeout} seconds')
                return False

    def _cleanup(self) -> None:
        self.slot = None
        self.callback = None
