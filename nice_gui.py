#!/usr/bin/env python3
import traceback
import justpy as jp
from starlette.applications import Starlette
import uvicorn
import inspect
import time
import asyncio
from contextlib import contextmanager
from matplotlib import pyplot as plt
from utils import handle_exceptions, provide_arguments
import icecream

icecream.install()

wp = jp.QuasarPage(delete_flag=False, title='Nice GUI', favicon='favicon.png')
main = jp.Div(a=wp, classes='q-ma-md column items-start', style='row-gap: 1em')
main.add_page(wp)
jp.justpy(lambda: wp, start_server=False)

view_stack = [main]

class Element:

    def __init__(self, view: jp.HTMLBaseComponent):

        view_stack[-1].add(view)
        view.add_page(wp)
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

    def switch(self, text, on_change=None):

        view = jp.QToggle(text=text)
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

    def slider(self, min, max, on_change=None):

        view = jp.QSlider(min=min, max=max)
        if on_change is not None:
            view.on('input', handle_exceptions(provide_arguments(on_change, 'value')))
        return Element(view)

    def input(self, placeholder=None, value=None, type='text', on_change=None):

        view = jp.QInput(placeholder=placeholder, type=type)
        if value is not None:
            view.value = value
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

        view = jp.QDiv(classes='row items-start', style='gap: 1em', delete_flag=False)
        return Element(view)

    def column(self):

        view = jp.QDiv(classes='column items-start', style='gap: 1em', delete_flag=False)
        return Element(view)

    def card(self):

        view = jp.QCard(classes='column items-start q-pa-md', style='gap: 1em', delete_flag=False)
        return Element(view)

    def timer(self, interval, callback, *, once=False):

        parent = view_stack[-1]

        async def timeout():

            await asyncio.sleep(interval)
            handle_exceptions(callback)()
            await main.update()

        async def loop():

            while True:
                try:
                    start = time.time()
                    handle_exceptions(callback)()
                    await parent.update()
                    dt = time.time() - start
                    await asyncio.sleep(interval - dt)
                except:
                    traceback.print_exc()
                    await asyncio.sleep(interval)

        jp.run_task(timeout() if once else loop())

    def run(self):

        # NOTE: prevent reloader from restarting uvicorn
        if inspect.stack()[-2].filename.endswith('spawn.py'):
            return

        uvicorn.run('nice_gui:ui', host='0.0.0.0', port=80, lifespan='on', reload=True)

# NOTE: instantiate our own ui object with all capabilities of jp.app
ui = Ui()
ui.__dict__.update(jp.app.__dict__)
