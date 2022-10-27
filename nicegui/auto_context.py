import asyncio
from contextlib import contextmanager
from typing import TYPE_CHECKING, Awaitable, Callable, Dict, Generator, List, Optional, Union

from . import globals
from .task_logger import create_task


def get_task_id() -> int:
    return id(asyncio.current_task()) if globals.loop and globals.loop.is_running() else 0


def get_view_stack() -> List['jp.HTMLBaseComponent']:
    task_id = get_task_id()
    if task_id not in globals.view_stacks:
        globals.view_stacks[task_id] = []
    return globals.view_stacks[task_id]


def prune_view_stack() -> None:
    task_id = get_task_id()
    if not globals.view_stacks[task_id]:
        del globals.view_stacks[task_id]


class within_view(object):
    def __init__(self, view: 'jp.HTMLBaseComponent'):
        self.view = view

    def __enter__(self):
        self.child_count = len(self.view)
        get_view_stack().append(self.view)
        return self

    def __exit__(self, type, value, traceback):
        get_view_stack().pop()
        prune_view_stack()
        self.lazy_update()

    def lazy_update(self):
        if len(self.view) != self.child_count:
            self.child_count = len(self.view)
            create_task(self.view.update())
