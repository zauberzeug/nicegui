"""inspired from https://quantlane.com/blog/ensure-asyncio-task-exceptions-get-logged/"""
import asyncio
from collections.abc import Awaitable, Callable, Coroutine, Generator
from typing import Any, TypeVar, cast, overload

from . import core, helpers
from .logging import log

running_tasks: set[asyncio.Task] = set()
lazy_tasks_running: dict[str, asyncio.Task] = {}
lazy_coroutines_waiting: dict[str, Coroutine[Any, Any, Any]] = {}
_await_tasks_on_shutdown: set[asyncio.Task] = set()


@overload
def create(awaitable: Awaitable[Any], *, name: str = 'unnamed task',
           handle_exceptions: bool = True) -> asyncio.Task: ...


@overload
def create(*, coroutine: Awaitable[Any], name: str = 'unnamed task',
           handle_exceptions: bool = True) -> asyncio.Task: ...


def create(awaitable: Awaitable[Any] | None = None, *, name: str = 'unnamed task',
           handle_exceptions: bool = True, coroutine: Awaitable[Any] | None = None) -> asyncio.Task:
    """Wraps a loop.create_task call and ensures there is an exception handler added to the task.

    Also a reference to the task is kept until it is done, so that the task is not garbage collected mid-execution.
    See https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task.

    :param awaitable: the awaitable to wrap
    :param coroutine: deprecated alias for ``awaitable``; will be removed in NiceGUI 4.0
    :param name: the name of the task which is helpful for debugging (default: "unnamed task")
    :param handle_exceptions: if ``True`` (default) possible exceptions are forwarded to the global exception handlers
    """
    awaitable = _resolve_awaitable(awaitable, coroutine, function_name='create')
    assert core.loop is not None
    coroutine = _ensure_coroutine(awaitable)
    task: asyncio.Task = core.loop.create_task(coroutine, name=name)
    if handle_exceptions:
        task.add_done_callback(_handle_exceptions)
    running_tasks.add(task)
    task.add_done_callback(running_tasks.discard)
    if isinstance(awaitable, _AwaitOnShutdown):
        _await_tasks_on_shutdown.add(task)
        task.add_done_callback(_await_tasks_on_shutdown.discard)
    return task


def create_or_defer(awaitable: Awaitable, *, name: str = 'unnamed task') -> asyncio.Task | None:
    """Create a background task, or defer to app startup if the event loop isn't running yet.

    :param awaitable: the awaitable to schedule
    :param name: the name of the task which is helpful for debugging (default: "unnamed task")
    :return: the created task, or ``None`` if deferred to startup
    """
    if core.can_schedule_task():
        return create(awaitable, name=name)
    core.app.on_startup(lambda: create(awaitable, name=name))
    return None


@overload
def create_lazy(awaitable: Awaitable[Any], *, name: str) -> None: ...


@overload
def create_lazy(*, coroutine: Awaitable[Any], name: str) -> None: ...


def create_lazy(awaitable: Awaitable[Any] | None = None, *, name: str,
                coroutine: Awaitable[Any] | None = None) -> None:
    """Wraps a create call and ensures a second task with the same name is delayed until the first one is done.

    If a third task with the same name is created while the first one is still running, the second one is discarded.
    """
    awaitable = _resolve_awaitable(awaitable, coroutine, function_name='create_lazy')
    if name in lazy_tasks_running:
        if name in lazy_coroutines_waiting:
            lazy_coroutines_waiting[name].close()
        lazy_coroutines_waiting[name] = _ensure_coroutine(awaitable)
        return

    def finalize(_) -> None:
        lazy_tasks_running.pop(name)
        if name in lazy_coroutines_waiting:
            create_lazy(lazy_coroutines_waiting.pop(name), name=name)

    task = create(awaitable, name=name)
    lazy_tasks_running[name] = task
    task.add_done_callback(finalize)


def create_lazy_or_defer(awaitable: Awaitable, *, name: str) -> None:
    """Create a lazy task, or defer to app startup if the event loop isn't running yet."""
    if core.can_schedule_task():
        create_lazy(awaitable, name=name)
    else:
        core.app.on_startup(lambda: create_lazy(awaitable, name=name))


class _AwaitOnShutdown:
    def __init__(self, factory: Callable[[], Awaitable[Any]]) -> None:
        self._factory = factory

    def __await__(self) -> Generator[Any, None, Any]:
        return self._factory().__await__()


F = TypeVar('F', bound=Callable[..., Awaitable[Any]])


def await_on_shutdown(func: F) -> F:
    """Tag an async function so tasks created from it won't be cancelled during shutdown.

    *Added in version 2.16.0*
    """

    def wrapper(*args: Any, **kwargs: Any) -> Awaitable[Any]:
        return _AwaitOnShutdown(lambda: func(*args, **kwargs))

    return cast(F, wrapper)


def _ensure_coroutine(awaitable: Awaitable[Any]) -> Coroutine[Any, Any, Any]:
    """Convert an awaitable to a coroutine if it isn't already one."""
    if asyncio.iscoroutine(awaitable):
        return awaitable

    async def wrapper() -> Any:
        return await awaitable

    return wrapper()


# DEPRECATED: remove `coroutine` keyword aliases in NiceGUI 4.0
def _resolve_awaitable(awaitable: Awaitable[Any] | None, coroutine: Awaitable[Any] | None, *,
                       function_name: str) -> Awaitable[Any]:
    if awaitable is None:
        if coroutine is None:
            raise TypeError(f"{function_name}() missing 1 required argument: 'awaitable'")
        helpers.warn_once(
            f'Using `{function_name}(coroutine=...)` is deprecated and will be removed in NiceGUI 4.0. '
            f'Use `{function_name}(awaitable=...)` instead.',
        )
        return coroutine
    if coroutine is not None:
        raise TypeError(f'{function_name}() received both awaitable and deprecated coroutine arguments')
    return awaitable


def _handle_exceptions(task: asyncio.Task) -> None:
    try:
        task.result()
    except asyncio.CancelledError:
        pass
    except Exception as e:
        core.app.handle_exception(e)


async def teardown() -> None:
    """Cancel all running tasks and coroutines on shutdown. (For internal use only.)"""
    while running_tasks or lazy_tasks_running:
        tasks = running_tasks | set(lazy_tasks_running.values())
        for task in tasks:
            if task.done() or task.cancelled() or task in _await_tasks_on_shutdown:
                continue
            task.cancel()
        if tasks:
            await asyncio.sleep(0)  # NOTE: ensure the loop can cancel the tasks before it shuts down
            try:
                await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), timeout=2.0)
            except asyncio.TimeoutError:
                log.error('Could not cancel %s tasks within timeout: %s',
                          len(tasks),
                          ', '.join(t.get_name() for t in tasks if not t.done()))
            except Exception:
                log.exception('Error while cancelling tasks')
    for coro in lazy_coroutines_waiting.values():
        coro.close()
