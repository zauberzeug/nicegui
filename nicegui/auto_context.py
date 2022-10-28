from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Coroutine, Generator, List

from . import globals
from .task_logger import create_task

if TYPE_CHECKING:
    import justpy as jp


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


class Context:

    def __init__(self, view: 'jp.HTMLBaseComponent') -> None:
        self.view = view

    def __enter__(self):
        self.child_count = len(self.view)
        get_view_stack().append(self.view)
        return self

    def __exit__(self, type, value, traceback):
        get_view_stack().pop()
        prune_view_stack()
        self.lazy_update()

    def lazy_update(self) -> None:
        if len(self.view) != self.child_count:
            self.child_count = len(self.view)
            create_task(self.view.update())

    def watch_asyncs(self, coro: Coroutine) -> AutoUpdaterForAsyncs:
        return AutoUpdaterForAsyncs(coro, self)


class AutoUpdaterForAsyncs:

    def __init__(self, coro: Coroutine, context: Context) -> None:
        self.coro = coro
        self.context = context
        self.context.lazy_update()

    def __await__(self) -> Generator[Any, None, Any]:
        coro_iter = self.coro.__await__()
        iter_send, iter_throw = coro_iter.send, coro_iter.throw
        send, message = iter_send, None
        while True:
            try:
                signal = send(message)
                self.context.lazy_update()
            except StopIteration as err:
                return err.value
            else:
                send = iter_send
            try:
                message = yield signal
            except BaseException as err:
                send, message = iter_throw, err
