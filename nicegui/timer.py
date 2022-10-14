import asyncio
import time
import traceback
from collections import namedtuple
from typing import Callable, List, Optional

from starlette.websockets import WebSocket

from . import globals
from .binding import BindableProperty
from .helpers import is_coroutine
from .page import Page, find_parent_page, find_parent_view
from .task_logger import create_task

NamedCoroutine = namedtuple('NamedCoroutine', ['name', 'coro'])


class Timer:
    prepared_coroutines: List[NamedCoroutine] = []

    active = BindableProperty()
    interval = BindableProperty()

    def __init__(self, interval: float, callback: Callable, *, active: bool = True, once: bool = False):
        """Timer

        One major drive behind the creation of NiceGUI was the necessity to have a simple approach to update the interface in regular intervals, for example to show a graph with incomming measurements.
        A timer will execute a callback repeatedly with a given interval.

        :param interval: the interval in which the timer is called (can be changed during runtime)
        :param callback: function or coroutine to execute when interval elapses
        :param active: whether the callback should be executed or not (can be changed during runtime)
        :param once: whether the callback is only executed once after a delay specified by `interval` (default: `False`)
        """

        self.active = active
        self.interval = interval
        self.socket: Optional[WebSocket] = None
        self.parent_page = find_parent_page()
        self.parent_view = find_parent_view()

        async def do_callback():
            try:
                with globals.within_view(self.parent_view):
                    result = callback()
                    if is_coroutine(callback):
                        await result
            except Exception:
                traceback.print_exc()

        async def timeout():
            await asyncio.sleep(self.interval)
            await do_callback()

        async def loop():
            while True:
                if not self.parent_page.shared:
                    sockets = list(Page.sockets.get(self.parent_page.page_id, {}).values())
                    if not self.socket and sockets:
                        self.socket = sockets[0]
                    elif self.socket and not sockets:
                        return
                try:
                    start = time.time()
                    if self.active:
                        await do_callback()
                    dt = time.time() - start
                    await asyncio.sleep(self.interval - dt)
                except asyncio.CancelledError:
                    return
                except:
                    traceback.print_exc()
                    await asyncio.sleep(self.interval)

        coroutine = timeout() if once else loop()
        if not (globals.loop and globals.loop.is_running()):
            self.prepared_coroutines.append(NamedCoroutine(str(callback), coroutine))
        else:
            globals.tasks.append(create_task(coroutine, name=str(callback)))
