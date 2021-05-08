#!/usr/bin/env python3
import justpy as jp
from starlette.applications import Starlette
import uvicorn
import inspect

wp = jp.WebPage(delete_flag=False)
jp.justpy(lambda: wp, start_server=False)

class Ui(Starlette):

    def label(self, text):

        jp.Div(text=text, a=wp)

    def run(self):

        # NOTE: prevent reloader to restart uvicorn
        if inspect.stack()[-2].filename.endswith('spawn.py'):
            return

        uvicorn.run('nice_gui:ui', host='0.0.0.0', port=80, lifespan='on', reload=True)

# NOTE: instantiate our own ui object with all capabilities of jp.app
ui = Ui()
ui.__dict__.update(jp.app.__dict__)
