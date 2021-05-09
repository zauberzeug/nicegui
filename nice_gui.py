#!/usr/bin/env python3
import justpy as jp
from starlette.applications import Starlette
import uvicorn
import inspect
import time
import asyncio
from utils import handle_exceptions, provide_arguments
import icecream

icecream.install()

wp = jp.WebPage(delete_flag=False, title='Nice GUI', favicon='favicon.png')
main = jp.Div(a=wp, classes='m-4 flex flex-col items-start gap-4')
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

class Ui(Starlette):

    def label(self, text=''):

        view = jp.Div(text=text)
        return Element(view)

    def button(self, text, on_click=None):

        view = jp.Button(text=text, classes='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded')
        if on_click is not None:
            view.on('click', handle_exceptions(provide_arguments(on_click)))
        return Element(view)

    def row(self):

        view = jp.Div(classes='flex flex-row gap-4 items-start')
        return Element(view)

    def column(self):

        view = jp.Div(classes='flex flex-col gap-4 items-start')
        return Element(view)

    def card(self):

        view = jp.Div(classes='flex flex-col gap-4 items-start p-4 rounded shadow-lg')
        return Element(view)

    def timer(self, inverval, callback):

        def update(view):
            if view.components:
                for v in view.components:
                    update(v)

            jp.run_task(view.update())

        async def loop():

            while True:
                start = time.time()
                handle_exceptions(callback)()
                update(view_stack[-1])
                dt = time.time() - start
                await asyncio.sleep(inverval - dt)

        jp.run_task(loop())

    def run(self):

        # NOTE: prevent reloader to restart uvicorn
        if inspect.stack()[-2].filename.endswith('spawn.py'):
            return

        uvicorn.run('nice_gui:ui', host='0.0.0.0', port=80, lifespan='on', reload=True)

# NOTE: instantiate our own ui object with all capabilities of jp.app
ui = Ui()
ui.__dict__.update(jp.app.__dict__)
