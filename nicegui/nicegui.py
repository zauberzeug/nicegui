#!/usr/bin/env python3
from typing import Awaitable, Callable
import asyncio

from .ui import Ui  # NOTE: before justpy
import justpy as jp
from .timer import Timer
from . import globals
from . import binding


def create_task(coro):
    loop = asyncio.get_event_loop()
    return loop.create_task(coro)

tasks = []

@jp.app.on_event('startup')
def startup():
    tasks.extend(create_task(t) for t in Timer.tasks)
    tasks.extend(create_task(t) for t in Ui.startup_tasks if isinstance(t, Awaitable))
    [t() for t in Ui.startup_tasks if isinstance(t, Callable)]
    jp.run_task(binding.loop())

@jp.app.on_event('shutdown')
def shutdown():
    [create_task(t) for t in Ui.shutdown_tasks if isinstance(t, Awaitable)]
    [t() for t in Ui.shutdown_tasks if isinstance(t, Callable)]
    [t.cancel() for t in tasks]


app = globals.app = jp.app
ui = Ui()

page = ui.page('/')
page.__enter__()
jp.justpy(lambda: page, start_server=False)
