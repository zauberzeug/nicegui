import asyncio
import time
import traceback
from binding import BindableProperty
from .elements.element import Element
from .utils import handle_exceptions

class Timer:

    tasks = []

    active = BindableProperty

    def __init__(self, interval, callback, *, once=False):

        parent = Element.view_stack[-1]
        self.active = True

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
