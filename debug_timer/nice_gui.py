#!/usr/bin/env python3
import traceback
import justpy as jp
from starlette.applications import Starlette
import uvicorn
import inspect
import asyncio

pad = '*' * 80

wp = jp.WebPage(delete_flag=False, head_html='<script>confirm = () => true;</script>')

main = jp.Div(a=wp, text='Hello JustPy!')
main.add_page(wp)
jp.justpy(lambda: wp, start_server=False)

def label(text):

    print(pad, __name__, "label()")

    view = jp.Div(text=text)
    main.add(view)
    view.add_page(wp)

def timer():

    print(pad, __name__, "timer()")

    async def loop():

        while True:
            print(pad, __name__, "loop()", flush=True)
            await asyncio.sleep(1.0)

    try:
        jp.run_task(loop())
    except:
        traceback.print_exc()

def run():

    print(pad, __name__, "run()")

    if inspect.stack()[-2].filename.endswith('spawn.py'):
        print(pad, __name__, "RETURN FROM RUN")
        return

    print(pad, "START UVICORN")
    uvicorn.run('main:ui', host='0.0.0.0', port=80, lifespan='on', reload=True)

ui = jp.app
ui.label = label
ui.timer = timer
ui.run = run
