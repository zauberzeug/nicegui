import asyncio
import time
import traceback
from typing import Callable

from .. import globals
from ..binding import BindableProperty
from ..client import Client
from ..helpers import is_coroutine
from ..lifecycle import on_startup
from ..task_logger import create_task


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

        coroutine = self._run_once if once else self._run_in_loop
        if globals.state == globals.State.STARTED:
            globals.tasks.append(create_task(coroutine(), name=str(callback)))
        else:
            on_startup(coroutine)

    async def _run_once(self) -> None:
        with globals.get_client() as client, client.slot_stack[-1]:
            await asyncio.sleep(self.interval)
            await self._invoke_callback(client)

    async def _run_in_loop(self) -> None:
        with globals.get_client() as client, client.slot_stack[-1]:
            while True:
                if client.id not in globals.clients:
                    return
                try:
                    start = time.time()
                    if self.active:
                        await self._invoke_callback(client)
                    dt = time.time() - start
                    await asyncio.sleep(self.interval - dt)
                except asyncio.CancelledError:
                    return
                except:
                    traceback.print_exc()
                    await asyncio.sleep(self.interval)

    async def _invoke_callback(self, client: Client) -> None:
        try:
            result = self.callback()
            if is_coroutine(self.callback):
                await client.watch_asyncs(result)
        except Exception:
            traceback.print_exc()
