#!/usr/bin/env python3
import justpy as jp
from starlette.applications import Starlette
import uvicorn
import inspect
import time
import asyncio
from contextlib import contextmanager
from matplotlib import pyplot as plt
from utils import handle_exceptions, provide_arguments

wp = jp.QuasarPage(delete_flag=False, title='Nice GUI', favicon='favicon.png')
main = jp.Div(a=wp, classes='q-ma-md column items-start', style='row-gap: 1em')
jp.justpy(lambda: wp, start_server=False)

view_stack = [main]

class Element:

    def __init__(self, view: jp.HTMLBaseComponent):

        view_stack[-1].add(view)
        self.view = view

    @property
    def text(self):
        return self.view.text

    @text.setter
    def text(self, text):
        self.view.text = text

    def set_text(self, text):
        self.view.text = text

    def __enter__(self):

        view_stack.append(self.view)

    def __exit__(self, *_):

        view_stack.pop()

class Plot(Element):

    def update(self, close=True):

        self.view.set_figure(plt.gcf())
        if close:
            plt.close()

class Ui(Starlette):

    def label(self, text='', typography=[]):

        if isinstance(typography, str):
            typography = [typography]
        classes = ' '.join('text-' + t for t in typography)
        view = jp.Div(text=text, classes=classes)
        return Element(view)

    def button(self, text, on_click=None):

        view = jp.QBtn(text=text, color='primary')
        if on_click is not None:
            view.on('click', handle_exceptions(provide_arguments(on_click)))
        return Element(view)

    def checkbox(self, text, on_change=None):

        view = jp.QCheckbox(text=text)
        if on_change is not None:
            view.on('input', handle_exceptions(provide_arguments(on_change, 'value')))
        return Element(view)

    def radio(self, options, value=None, on_change=None):

        view = jp.QOptionGroup(value=value, options=[{'label': o, 'value': o} for o in options])
        if on_change is not None:
            view.on('input', handle_exceptions(provide_arguments(on_change, 'value')))
        return Element(view)

    def select(self, options, value=None, on_change=None):

        view = jp.QSelect(value=value, options=options)
        if on_change is not None:
            view.on('input', handle_exceptions(provide_arguments(on_change, 'value')))
        return Element(view)

    def switch(self, text, on_change=None):

        view = jp.QToggle(text=text)
        if on_change is not None:
            view.on('input', handle_exceptions(provide_arguments(on_change, 'value')))
        return Element(view)

    @contextmanager
    def plot(self, close=True):

        view = jp.Matplotlib()
        yield Plot(view)
        view.set_figure(plt.gcf())
        if close:
            plt.close()

    def row(self):

        view = jp.QDiv(classes='row items-start', style='column-gap: 1em')
        return Element(view)

    def column(self):

        view = jp.QDiv(classes='column items-start', style='row-gap: 1em')
        return Element(view)

    def card(self):

        view = jp.QCard(classes='q-pa-md column items-start', style='row-gap: 1em')
        return Element(view)

    def timer(self, interval, callback, *, once=False):

        async def timeout():

            await asyncio.sleep(interval)
            handle_exceptions(callback)()
            jp.run_task(wp.update())

        async def loop():

            while True:
                start = time.time()
                handle_exceptions(callback)()
                jp.run_task(wp.update())
                dt = time.time() - start
                await asyncio.sleep(interval - dt)

        jp.run_task(timeout() if once else loop())

    def run(self):

        # NOTE: prevent reloader from restarting uvicorn
        if inspect.stack()[-2].filename.endswith('spawn.py'):
            return

        uvicorn.run('nice_gui:ui', host='0.0.0.0', port=80, lifespan='on', reload=True)

# NOTE: instantiate our own ui object with all capabilities of jp.app
ui = Ui()
ui.__dict__.update(jp.app.__dict__)
