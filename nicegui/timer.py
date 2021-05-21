import asyncio
import time
import traceback
from binding import BindableProperty
from .elements.element import Element
from .utils import handle_exceptions

class Timer:

    tasks = []

    active = BindableProperty

    def __init__(self, interval, callback, *, active=True, once=False):
        """Timer

        One major drive behind the creation of NiceGUI was the necessity to have a simple approach to update the interface in regular intervals, for example to show a graph with incomming measurements.

        :param interval: the interval in which the timer is called
        :param callback: function to execute when interval elapses
        :param active: whether the callback should be executed or not
        :param once: whether the callback is only executed once after a delay specified by `interval`; default is `False`
        """

        parent = Element.view_stack[-1]
        self.active = active

        async def timeout():

            await asyncio.sleep(interval)
            handle_exceptions(callback)()
            await parent.update()

        async def loop():

            while True:
                try:
                    start = time.time()
                    if self.active:
                        handle_exceptions(callback)()
                        await parent.update()
                    dt = time.time() - start
                    await asyncio.sleep(interval - dt)
                except:
                    traceback.print_exc()
                    await asyncio.sleep(interval)

        self.tasks.append(timeout() if once else loop())
