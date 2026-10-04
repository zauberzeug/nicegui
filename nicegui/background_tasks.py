"""inspired from https://quantlane.com/blog/ensure-asyncio-task-exceptions-get-logged/"""
import asyncio
from collections.abc import Awaitable, Callable, Coroutine, Generator
from contextlib import AbstractContextManager, nullcontext, suppress
from typing import Any, TypeVar, cast, overload

from . import core
from .helpers.warnings import warn_once
from .logging import log
from .slot import Slot

running_tasks: set[asyncio.Task] = set()
lazy_tasks_running: dict[str, asyncio.Task] = {}
lazy_coroutines_waiting: dict[str, Awaitable[Any]] = {}
_await_tasks_on_shutdown: set[asyncio.Task] = set()
_deferred_awaitables: list[Awaitable[Any]] = []


@overload
def create(awaitable: Awaitable[Any], *, name: str = 'unnamed task',
           handle_exceptions: bool = True, context: AbstractContextManager | None = None) -> asyncio.Task: ...


@overload
def create(*, coroutine: Awaitable[Any], name: str = 'unnamed task',
           handle_exceptions: bool = True, context: AbstractContextManager | None = None) -> asyncio.Task: ...


def create(awaitable: Awaitable[Any] | None = None, *,
           coroutine: Awaitable[Any] | None = None,
           name: str = 'unnamed task',
           handle_exceptions: bool = True,
           context: AbstractContextManager | None = None) -> asyncio.Task:
    """Wraps a loop.create_task call and ensures there is an exception handler added to the task.

    Also a reference to the task is kept until it is done, so that the task is not garbage collected mid-execution.
    See https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task.

    :param awaitable: the awaitable to wrap
    :param coroutine: deprecated alias for ``awaitable``; will be removed in NiceGUI 4.0
    :param name: the name of the task which is helpful for debugging (default: "unnamed task")
    :param handle_exceptions: if ``True`` (default) possible exceptions are forwarded to the exception handlers
        (within the ``context`` if given, so that the client's handlers are reached as well; otherwise only the global ones)
    :param context: a context manager to await the awaitable in, e.g. a container element or ``ui.context.client``
        (default: ``None``, *added in version 3.18.0*)
    """
    awaitable = _resolve_awaitable(awaitable, coroutine, function_name='create')
    assert core.loop is not None
    if context is None:
        task = core.loop.create_task(_ensure_coroutine(awaitable), name=name)
        if handle_exceptions:
            task.add_done_callback(_handle_exceptions)
    else:
        client = None
        slots = [context] if isinstance(context, Slot) else Slot.get_stack()
        with suppress(RuntimeError):  # the element of the slot or its client may have been deleted
            if slots:
                client = slots[-1].parent.client  # resolve it now, because the element may be deleted while awaiting
        coro = _await_in_context(awaitable, context, client or nullcontext(), handle_exceptions=handle_exceptions)
        task = core.loop.create_task(coro, name=name)
        if handle_exceptions:
            task.add_done_callback(_retrieve_exception)  # the exception has already been handled in-context
        if asyncio.iscoroutine(awaitable):
            inner = awaitable
            # the task may have been cancelled before awaiting the coroutine
            task.add_done_callback(lambda _: inner.close())
    running_tasks.add(task)
    task.add_done_callback(running_tasks.discard)
    if isinstance(awaitable, _AwaitOnShutdown):
        _await_tasks_on_shutdown.add(task)
        task.add_done_callback(_await_tasks_on_shutdown.discard)
    return task


def create_or_defer(awaitable: Awaitable, *, name: str = 'unnamed task',
                    context: AbstractContextManager | None = None) -> None:
    """Create a background task, or defer to app startup if the event loop isn't running yet.

    :param awaitable: the awaitable to schedule
    :param name: the name of the task which is helpful for debugging (default: "unnamed task")
    :param context: a context manager to await the awaitable in, see ``create()`` (default: ``None``, *added in version 3.18.0*)
    """
    if core.is_loop_running():
        create(awaitable, name=name, context=context)
    else:
        _defer(awaitable, lambda: create(awaitable, name=name, context=context))


@overload
def create_lazy(awaitable: Awaitable[Any], *, name: str) -> None: ...


@overload
def create_lazy(*, coroutine: Awaitable[Any], name: str) -> None: ...


def create_lazy(awaitable: Awaitable[Any] | None = None, *,
                coroutine: Awaitable[Any] | None = None,
                name: str) -> None:
    """Wraps a create call and ensures a second task with the same name is delayed until the first one is done.

    If a third task with the same name is created while the first one is still running, the second one is discarded.
    """
    awaitable = _resolve_awaitable(awaitable, coroutine, function_name='create_lazy')
    if name in lazy_tasks_running:
        waiting = lazy_coroutines_waiting.get(name)
        if asyncio.iscoroutine(waiting):
            waiting.close()
        # NOTE: store the original awaitable so an _AwaitOnShutdown marker survives requeueing in finalize()
        lazy_coroutines_waiting[name] = awaitable
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
    if core.is_loop_running():
        create_lazy(awaitable, name=name)
    else:
        _defer(awaitable, lambda: create_lazy(awaitable, name=name))


def _defer(awaitable: Awaitable[Any], start: Callable[[], Any]) -> None:
    """Start the awaitable on app startup and remember it until then so that ``reset()`` can close it."""
    def start_deferred() -> None:
        if awaitable in _deferred_awaitables:
            _deferred_awaitables.remove(awaitable)
        start()
    core.app.on_startup(start_deferred)
    _deferred_awaitables.append(awaitable)


def reset() -> None:
    """Close awaitables which were deferred to app startup but will never be started. (Useful for testing.)

    Note: Call this together with ``app.reset()``,
    which drops the startup handlers that would otherwise start the closed awaitables.
    """
    for awaitable in _deferred_awaitables:
        if asyncio.iscoroutine(awaitable):
            awaitable.close()
    _deferred_awaitables.clear()


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
def _resolve_awaitable(awaitable: Awaitable[Any] | None,
                       coroutine: Awaitable[Any] | None, *,
                       function_name: str) -> Awaitable[Any]:
    if awaitable is None:
        if coroutine is None:
            raise TypeError(f'{function_name}() missing 1 required argument: "awaitable"')
        warn_once(f'Using `{function_name}(coroutine=...)` is deprecated and will be removed in NiceGUI 4.0. '
                  f'Use `{function_name}(awaitable=...)` instead.')
        return coroutine
    if coroutine is not None:
        raise TypeError(f'{function_name}() received both awaitable and deprecated coroutine arguments')
    return awaitable


async def _await_in_context(awaitable: Awaitable[Any], context: AbstractContextManager,
                            client: AbstractContextManager, *, handle_exceptions: bool) -> Any:
    """Await an awaitable within a context, handling exceptions in-context so that the client's handlers are reached."""
    with client, context:  # the client is still found if the element of the context is deleted while awaiting
        try:
            return await awaitable
        except Exception as e:
            if handle_exceptions:
                core.app.handle_exception(e)
            raise


def _retrieve_exception(task: asyncio.Task) -> None:
    """Mark the exception of a task as retrieved, because it has already been handled in-context."""
    if not task.cancelled():
        task.exception()


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
            await asyncio.sleep(0)  # ensure the loop can cancel the tasks before it shuts down
            try:
                await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), timeout=2.0)
            except asyncio.TimeoutError:
                log.error('Could not cancel %s tasks within timeout: %s',
                          len(tasks),
                          ', '.join(t.get_name() for t in tasks if not t.done()))
            except Exception:
                log.exception('Error while cancelling tasks')
    for awaitable in lazy_coroutines_waiting.values():
        if asyncio.iscoroutine(awaitable):
            awaitable.close()
