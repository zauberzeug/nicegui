import asyncio
from elements.element import Element

class Timer:

    tasks = []

    def __init__(self, interval, callback):

        parent = Element.view_stack[-1]

        async def loop():

            while True:
                callback()
                await parent.update()
                await asyncio.sleep(interval)

        self.tasks.append(loop())