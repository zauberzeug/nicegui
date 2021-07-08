#!/usr/bin/env python3
from typing import Awaitable, Callable
import os 
host = os.getenv('HOST', '0.0.0.0')
port = int(os.getenv('PORT', '80'))
os.environ['HOST'] = host
os.environ['PORT']= str(port)
import justpy as jp
import uvicorn
import sys
import inspect
import webbrowser
from pygments.formatters import HtmlFormatter
import binding
import asyncio
from .ui import Ui
from .timer import Timer
from .elements.element import Element
import atexit


os.environ["STATIC_DIRECTORY"] = os.path.dirname(os.path.realpath(__file__)) + '/static'
os.environ["TEMPLATES_DIRECTORY"] = os.environ["STATIC_DIRECTORY"] + '/templates'

if os.getenv('RELOAD', 'true').lower() in ('true', 't', 'y', 'yes', '1'):
    if not inspect.stack()[-2].filename.endswith('spawn.py'):
        webbrowser.open(f'http://{host}:{port}/')
        uvicorn.run('nicegui:app', host=host, port=port, lifespan='on', reload=True)
        sys.exit()
else:
    def start_web():
        webbrowser.open(f'http://{host}:{port}/')
        uvicorn.run(jp.app, host=host, port=port, lifespan='on')
       
    atexit.register(start_web)

@jp.SetRoute('/file')
def get_file(request):
    wp = jp.WebPage()
    with open(request.query_params.get('path')) as f:
        wp.html = f.read()
    return wp

wp = jp.QuasarPage(delete_flag=False, title='NiceGUI', favicon='favicon.png')
wp.tailwind = True  # use Tailwind classes instead of Quasars
wp.css = HtmlFormatter().get_style_defs('.codehilite')
wp.head_html += '<script>confirm = () => true;</script>\n'  # avoid confirmation dialog for reload

main = jp.Div(a=wp, classes='q-ma-md column items-start', style='row-gap: 1em')
main.add_page(wp)

jp.justpy(lambda: wp, start_server=False)

async def binding_loop():
    while True:
        binding.update()
        await asyncio.sleep(0.1)

def create_task(coro):
    loop = asyncio.get_event_loop()
    return loop.create_task(coro)

tasks = []

@jp.app.on_event('startup')
def startup():
    global tasks
    tasks += [create_task(t) for t in Timer.tasks]
    tasks += [create_task(t) for t in Ui.startup_tasks if isinstance(t, Awaitable)]
    [t() for t in Ui.startup_tasks if isinstance(t, Callable)]
    jp.run_task(binding_loop())

@jp.app.on_event('shutdown')
def shutdown():
    [create_task(t) for t in Ui.shutdown_tasks if isinstance(t, Awaitable)]
    [t() for t in Ui.shutdown_tasks if isinstance(t, Callable)]
    # # also abort all running startup tasks
    [t.cancel() for t in tasks]

Element.wp = wp
Element.view_stack = [main]

app = jp.app
ui = Ui()
