#!/usr/bin/env python3
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

# start uvicorn with auto-reload; afterwards the auto-reloaded process should not start uvicorn again
if not inspect.stack()[-2].filename.endswith('spawn.py'):
    webbrowser.open('http://localhost/')
    uvicorn.run('nicegui:app', host='0.0.0.0', port=80, lifespan='on', reload=True)
    sys.exit()

wp = jp.QuasarPage(delete_flag=False, title='NiceGUI', favicon='favicon.png')
wp.tailwind = True  # use Tailwind classes instead of Quasars
wp.css = HtmlFormatter().get_style_defs('.codehilite')
wp.head_html = '<script>confirm = () => true;</script>'  # avoid confirmation dialog for reload
wp.head_html += '<link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel="stylesheet">'  # using latest tailwind

main = jp.Div(a=wp, classes='q-ma-md column items-start', style='row-gap: 1em')
main.add_page(wp)
jp.justpy(lambda: wp, start_server=False)

async def binding_loop():
    while True:
        binding.update()
        await asyncio.sleep(0.1)

@jp.app.on_event('startup')
def startup():
    [jp.run_task(t) for t in Timer.tasks]
    jp.run_task(binding_loop())

Element.wp = wp
Element.view_stack = [main]

app = jp.app
ui = Ui()
