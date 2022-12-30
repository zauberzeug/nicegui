import asyncio
import time
import traceback
from typing import Callable

from .. import globals
from ..async_updater import AsyncUpdater
from ..binding import BindableProperty
from ..helpers import is_coroutine
from ..task_logger import create_task
from .lifecycle import on_startup


class Timer:
    active = BindableProperty()
    interval = BindableProperty()

    def __init__(self, interval: float, callback: Callable, *, active: bool = True, once: bool = False) -> None:
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
        self.callback = callback
        self.active = active
        self.slot = globals.get_slot()

        coroutine = self._run_once if once else self._run_in_loop
        if globals.state == globals.State.STARTED:
            globals.tasks.append(create_task(coroutine(), name=str(callback)))
        else:
            on_startup(coroutine)

    async def _run_once(self) -> None:
        with self.slot:
            await self._handshake()
            await asyncio.sleep(self.interval)
            await self._invoke_callback()
        self.cleanup()

    async def _run_in_loop(self) -> None:
        with self.slot:
            await self._handshake()
            while True:
                if self.slot.parent.client.id not in globals.clients:
                    break
                try:
                    start = time.time()
                    if self.active:
                        await self._invoke_callback()
                    dt = time.time() - start
                    await asyncio.sleep(self.interval - dt)
                except asyncio.CancelledError:
                    break
                except:
                    globals.log.exception('Exception in timer callback')
                    await asyncio.sleep(self.interval)
        self.cleanup()

    async def _invoke_callback(self) -> None:
        try:
            result = self.callback()
            if is_coroutine(self.callback):
                await AsyncUpdater(result)
        except Exception:
            traceback.print_exc()

    async def _handshake(self) -> None:
        '''Wait for the client handshake before the timer callback can can be allowed to manipulate the state.
        See https://github.com/zauberzeug/nicegui/issues/206 for details.
        '''
        if not self.slot.parent.client.shared:
            await self.slot.parent.client.handshake()

    def cleanup(self) -> None:
        self.slot = None
        self.callback = None
