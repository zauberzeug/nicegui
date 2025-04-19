"""inspired from https://quantlane.com/blog/ensure-asyncio-task-exceptions-get-logged/"""
from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Coroutine, Dict, Set

from . import core

running_tasks: Set[asyncio.Task] = set()
lazy_tasks_running: Dict[str, asyncio.Task] = {}
lazy_coroutines_waiting: Dict[str, Coroutine[Any, Any, Any]] = {}


def create(coroutine: Awaitable, *, name: str = 'unnamed task') -> asyncio.Task:
    """Wraps a loop.create_task call and ensures there is an exception handler added to the task.

    If the task raises an exception, it is logged and handled by the global exception handlers.
    Also a reference to the task is kept until it is done, so that the task is not garbage collected mid-execution.
    See https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task.
    """
    assert core.loop is not None
    coroutine = coroutine if asyncio.iscoroutine(coroutine) else asyncio.wait_for(coroutine, None)
    task: asyncio.Task = core.loop.create_task(coroutine, name=name)
    task.add_done_callback(_handle_task_result)
    running_tasks.add(task)
    task.add_done_callback(running_tasks.discard)
    return task


def create_lazy(awaitable: Awaitable, *, name: str) -> None:
    """Wraps a create call and ensures a second task with the same name is delayed until the first one is done.

    If a third task with the same name is created while the first one is still running, the second one is discarded.
    """
    if name in lazy_tasks_running:
        if name in lazy_coroutines_waiting:
            lazy_coroutines_waiting[name].close()
        lazy_coroutines_waiting[name] = _ensure_coroutine(awaitable)
        return

    def finalize(name: str) -> None:
        lazy_tasks_running.pop(name)
        if name in lazy_coroutines_waiting:
            create_lazy(lazy_coroutines_waiting.pop(name), name=name)
    task = create(awaitable, name=name)
    lazy_tasks_running[name] = task
    task.add_done_callback(lambda _: finalize(name))


def _ensure_coroutine(awaitable: Awaitable[Any]) -> Coroutine[Any, Any, Any]:
    """Convert an awaitable to a coroutine if it isn't already one."""
    if asyncio.iscoroutine(awaitable):
        return awaitable

    async def wrapper() -> Any:
        return await awaitable
    return wrapper()


def _handle_task_result(task: asyncio.Task) -> None:
    try:
        task.result()
    except asyncio.CancelledError:
        pass
    except Exception as e:
        core.app.handle_exception(e)


async def on_shutdown() -> None:
    """Cancel all running tasks and coroutines on shutdown."""
    for task in list(running_tasks):
        await _cancel_task(task)
    for task in list(lazy_tasks_running.values()):
        await _cancel_task(task)
    for coroutine in lazy_coroutines_waiting.values():
        coroutine.close()


async def _cancel_task(task: asyncio.Task) -> None:
    task.cancel()
    try:
        await task  # NOTE we must run the task to completion
    except asyncio.CancelledError:
        pass
