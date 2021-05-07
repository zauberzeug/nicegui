import justpy as jp
from contextlib import contextmanager
import asyncio
import time
from utils import handle_exceptions, provide_sender

class Group:

    def label(self, text) -> jp.Div:

        return jp.Div(text=text, a=self.view, classes='')

    def button(self, text, on_click=None) -> jp.Button:

        b = jp.Button(text=text, a=self.view, classes='p-2 w-48 bg-blue-700 text-white text-center')
        if on_click is not None:
            b.on('click', handle_exceptions(provide_sender(on_click, self)))
        return b

    @contextmanager
    def plot(self):

        yield
        jp.Matplotlib(a=self.view)

    @contextmanager
    def column(self):

        yield Column(self.view)

    @contextmanager
    def row(self):

        yield Row(self.view)

    def timer(self, inverval, callback):

        async def loop():

            while True:
                start = time.time()
                handle_exceptions(callback)()
                jp.run_task(self.view.update())
                dt = time.time() - start
                await asyncio.sleep(inverval - dt)

        jp.run_task(loop())


class Page(Group):

    def __init__(self):

        self.view = jp.WebPage(delete_flag=False, body_classes='m-4', title='Nice GUI', favicon='favicon.png')


class Column(Group):

    def __init__(self, parent_view) -> None:

        self.view = jp.Div(a=parent_view, classes='flex flex-col gap-4 items-start')


class Row(Group):

    def __init__(self, parent_view) -> None:

        self.view = jp.Div(a=parent_view, classes='flex flex-row flex-wrap gap-4 items-start')