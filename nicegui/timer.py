import asyncio
import time
import traceback
from typing import Awaitable, Callable, Union
from binding import BindableProperty
from .elements.element import Element
from .utils import handle_exceptions, handle_awaitable

class Timer:

    tasks = []

    active = BindableProperty

    def __init__(self, interval: float, callback: Union[Callable, Awaitable], *, active: bool = True, once: bool = False):
        """Timer

        One major drive behind the creation of NiceGUI was the necessity to have a simple approach to update the interface in regular intervals, for example to show a graph with incomming measurements.
        A timer will execute a callback repeatedly with a given interval.
        The parent view container will be updated automatically, as long as the callback does not return `False`.

        :param interval: the interval in which the timer is called
        :param callback: function or coroutine to execute when interval elapses (can return `False` to prevent view update)
        :param active: whether the callback should be executed or not
        :param once: whether the callback is only executed once after a delay specified by `interval`; default is `False`
        """

        parent = Element.view_stack[-1]
        self.active = active

        async def timeout():

            await asyncio.sleep(interval)
            await handle_exceptions(handle_awaitable(callback))()
            await parent.update()

        async def loop():

            while True:
                try:
                    start = time.time()
                    if self.active:
                        needs_update = await handle_exceptions(handle_awaitable(callback))()
                        if needs_update != False:
                            await parent.update()
                    dt = time.time() - start
                    await asyncio.sleep(interval - dt)
                except asyncio.CancelledError:
                    pass
                except:
                    traceback.print_exc()
                    await asyncio.sleep(interval)

        self.tasks.append(timeout() if once else loop())
