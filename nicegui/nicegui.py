#!/usr/bin/env python3
from typing import Awaitable, Callable
import asyncio
import binding
from pygments.formatters import HtmlFormatter
from .ui import Ui  # NOTE: before justpy
import justpy as jp
from .elements.element import Element
from .timer import Timer

wp = jp.QuasarPage(delete_flag=False, title=Ui.config.title, favicon=Ui.config.favicon)
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
    tasks.extend(create_task(t) for t in Timer.tasks)
    tasks.extend(create_task(t) for t in Ui.startup_tasks if isinstance(t, Awaitable))
    [t() for t in Ui.startup_tasks if isinstance(t, Callable)]
    jp.run_task(binding_loop())

@jp.app.on_event('shutdown')
def shutdown():
    [create_task(t) for t in Ui.shutdown_tasks if isinstance(t, Awaitable)]
    [t() for t in Ui.shutdown_tasks if isinstance(t, Callable)]
    [t.cancel() for t in tasks]

Element.wp = wp
Element.view_stack = [main]

app = jp.app
ui = Ui()
