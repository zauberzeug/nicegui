#!/usr/bin/env python3
from typing import Awaitable, Callable
import asyncio
import binding

from .ui import Ui  # NOTE: before justpy
import justpy as jp
from .timer import Timer


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


app = jp.app
ui = Ui(app)

ui.page.default_title = ui.config.title
ui.page.default_favicon = ui.config.favicon
page = ui.page('/')
page.__enter__()
jp.justpy(lambda: page, start_server=False)
