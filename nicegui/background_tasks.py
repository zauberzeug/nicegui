"""inspired from https://quantlane.com/blog/ensure-asyncio-task-exceptions-get-logged/"""
import asyncio
import sys
from typing import Awaitable, Dict, Set, TypeVar

from . import globals

T = TypeVar('T')

name_supported = sys.version_info[1] >= 8

running_tasks: Set[asyncio.Task] = set()
lazy_tasks_running: Dict[str, asyncio.Task] = {}
lazy_tasks_waiting: Dict[str, Awaitable[T]] = {}


def create(coroutine: Awaitable[T], *, name: str = 'unnamed task') -> 'asyncio.Task[T]':
    """Wraps a loop.create_task call and ensures there is an exception handler added to the task.

    If the task raises an exception, it is logged and handled by the global exception handlers.
    Also a reference to the task is kept until it is done, so that the task is not garbage collected mid-execution.
    See https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task.
    """
    assert globals.loop is not None
    task: asyncio.Task = \
        globals.loop.create_task(coroutine, name=name) if name_supported else globals.loop.create_task(coroutine)
    task.add_done_callback(_handle_task_result)
    running_tasks.add(task)
    task.add_done_callback(running_tasks.discard)
    return task


def create_lazy(coroutine: Awaitable[T], *, name: str) -> None:
    """Wraps a create call and ensures a second task with the same name is delayed until the first one is done.

    If a third task with the same name is created while the first one is still running, the second one is discarded.
    """
    if name in lazy_tasks_running:
        if name in lazy_tasks_waiting:
            asyncio.Task(lazy_tasks_waiting[name]).cancel()
        lazy_tasks_waiting[name] = coroutine
        return

    def finalize(name: str) -> None:
        lazy_tasks_running.pop(name)
        if name in lazy_tasks_waiting:
            create_lazy(lazy_tasks_waiting.pop(name), name=name)
    task = create(coroutine, name=name)
    lazy_tasks_running[name] = task
    task.add_done_callback(lambda _: finalize(name))


def _handle_task_result(task: asyncio.Task) -> None:
    try:
        task.result()
    except asyncio.CancelledError:
        pass
    except Exception as e:
        globals.handle_exception(e)
