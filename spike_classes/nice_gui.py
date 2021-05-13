#!/usr/bin/env python3
import justpy as jp
import uvicorn
import sys
import inspect
from ui import Ui
from timer import Timer
from elements.element import Element

if not inspect.stack()[-2].filename.endswith('spawn.py'):
    uvicorn.run('nice_gui:app', host='0.0.0.0', port=80, lifespan='on', reload=True)
    sys.exit()

wp = jp.QuasarPage(delete_flag=False, head_html='<script>confirm = () => true;</script>')

main = jp.Div(a=wp, classes='q-ma-md column items-start', style='row-gap: 1em')
main.add_page(wp)
jp.justpy(lambda: wp, start_server=False)

@jp.app.on_event('startup')
def startup():
    [jp.run_task(t) for t in Timer.tasks]

Element.view_stack = [main]
Element.wp = wp

app = jp.app
ui = Ui
