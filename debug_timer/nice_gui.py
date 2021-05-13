#!/usr/bin/env python3
import traceback
import justpy as jp
from starlette.applications import Starlette
import uvicorn
import inspect
import asyncio

pad = '*' * 80

if not inspect.stack()[-2].filename.endswith('spawn.py'):
    print(pad, "START UVICORN")
    uvicorn.run('nice_gui:ui', host='0.0.0.0', port=80, lifespan='on', reload=True)

wp = jp.WebPage(delete_flag=False, head_html='<script>confirm = () => true;</script>')

main = jp.Div(a=wp, text='Hello JustPy!')
main.add_page(wp)
jp.justpy(lambda: wp, start_server=False)

class Ui(Starlette):

    def __init__(self):

        self.__dict__.update(jp.app.__dict__)

        self.tasks = []

        @self.on_event('startup')
        def startup():

            print(pad, __name__, "startup()")
            [jp.run_task(t) for t in self.tasks]

    def label(self, text):

        print(pad, __name__, "label()")

        view = jp.Div(text=text)
        main.add(view)
        view.add_page(wp)

    def timer(self):

        print(pad, __name__, "timer()")

        async def loop():

            while True:
                print(pad, __name__, "loop()", flush=True)
                await asyncio.sleep(1.0)

        self.tasks.append(loop())

ui = Ui()

