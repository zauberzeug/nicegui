import asyncio
import time
import traceback
from typing import Awaitable, Callable, List, Union
from collections import namedtuple

from .binding import BindableProperty
from .globals import tasks, view_stack
from .task_logger import create_task

NamedCoroutine = namedtuple('NamedCoroutine', ['name', 'coro'])

class Timer:
    prepared_coroutines: List[NamedCoroutine] = []

    active = BindableProperty()

    def __init__(self, interval: float, callback: Union[Callable, Awaitable], *, active: bool = True, once: bool = False):
        """Timer

        One major drive behind the creation of NiceGUI was the necessity to have a simple approach to update the interface in regular intervals, for example to show a graph with incomming measurements.
        A timer will execute a callback repeatedly with a given interval.
        The parent view container will be updated automatically, as long as the callback does not return `False`.

        :param interval: the interval in which the timer is called
        :param callback: function or coroutine to execute when interval elapses (can return `False` to prevent view update)
        :param active: whether the callback should be executed or not
        :param once: whether the callback is only executed once after a delay specified by `interval` (default: `False`)
        """

        parent = view_stack[-1]
        self.active = active

        async def do_callback():
            try:
                if asyncio.iscoroutinefunction(callback):
                    return await callback()
                else:
                    return callback()
            except Exception:
                traceback.print_exc()

        async def timeout():
            await asyncio.sleep(interval)
            await do_callback()
            await parent.update()

        async def loop():
            while True:
                try:
                    start = time.time()
                    if self.active:
                        needs_update = await do_callback()
                        if needs_update != False:
                            await parent.update()
                    dt = time.time() - start
                    await asyncio.sleep(interval - dt)
                except asyncio.CancelledError:
                    pass
                except:
                    traceback.print_exc()
                    await asyncio.sleep(interval)

        coroutine = timeout() if once else loop()
        event_loop = asyncio.get_event_loop()
        if not event_loop.is_running():
            self.prepared_coroutines.append(NamedCoroutine(str(callback), coroutine))
        else:
            tasks.append(create_task(coroutine, name=str(callback)))
