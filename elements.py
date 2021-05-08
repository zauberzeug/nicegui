import justpy as jp
from typing import List
from contextlib import contextmanager
import asyncio
import time
import uuid
from utils import handle_exceptions, provide_arguments

class Group:

    def label(self, text) -> jp.Div:

        return jp.Div(text=text, a=self.view, classes='')

    def button(self, text, on_click=None) -> jp.Button:

        b = jp.Button(text=text, a=self.view, classes='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded')
        if on_click is not None:
            b.on('click', handle_exceptions(provide_arguments(on_click)))
        return b

    def checkbox(self, text=None, on_change=None) -> jp.Input:

        d = jp.Div(a=self.view, classes='flex gap-4')
        c = jp.Input(a=d, type='checkbox', classes='form-checkbox mt-1 ml-4')
        if text is not None:
            jp.Div(text=text, a=d)
        if on_change is not None:
            c.on('change', handle_exceptions(provide_arguments(on_change, 'checked')))
        return d
    
    def select(self, options: List[str], value=None, on_change=None) -> jp.Input:

        s = jp.Select(classes='p-2 border rounded', a=self.view, value=value)
        if on_change is not None:
            s.on('change', handle_exceptions(provide_arguments(on_change, 'value')))
        [ jp.Option(value=option, text=option, a=s) for option in options]
        return s
    
    def radio(self, options: List[str], value=None, vertical=False, on_change=None) -> jp.Input:

        flex_direction = 'flex-col' if vertical else 'flex-row'
        name = str(uuid.uuid4())
        outer = jp.Div(a=self.view, classes=f'flex gap-2 {flex_direction}')
        for option in options:
            inner = jp.Label(classes='inline-block', a=outer)
            r = jp.Input(type='radio', name=name, value=option, checked=option==value, a=inner, classes='mx-2')
            r.on('change', handle_exceptions(provide_arguments(on_change, 'value')))
            jp.Span(a=inner, text=option)
        
        return outer

    @contextmanager
    def plot(self):

        yield
        jp.Matplotlib(a=self.view)

    @contextmanager
    def card(self):

        yield Card(self)

    @contextmanager
    def column(self):

        yield Column(self)

    @contextmanager
    def row(self):

        yield Row(self)

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


class Card(Group):

    def __init__(self, parent) -> None:

        self.parent = parent
        self.view = jp.Div(a=parent.view, classes='p-4 flex flex-col gap-4 items-start rounded shadow-lg')


class Column(Group):

    def __init__(self, parent) -> None:

        self.parent = parent
        self.view = jp.Div(a=parent.view, classes='flex flex-col gap-4 items-start')


class Row(Group):

    def __init__(self, parent) -> None:

        self.parent = parent
        self.view = jp.Div(a=parent.view, classes='flex flex-row flex-wrap gap-4 items-start')