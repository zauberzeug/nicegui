from __future__ import annotations

import asyncio
import inspect
import weakref
from collections.abc import Awaitable, Callable
from contextlib import nullcontext
from dataclasses import dataclass
from typing import Any, ClassVar, Generic
from weakref import WeakSet

from typing_extensions import ParamSpec

from . import background_tasks, core, helpers
from .client import Client
from .context import context
from .slot import Slot

P = ParamSpec('P')


@dataclass(kw_only=True, slots=True)
class Callback(Generic[P]):
    func: Callable[P, Any] | Callable[[], Any]
    expect_args: bool
    filepath: str
    line: int
    slot: weakref.ref[Slot] | None = None

    def run(self, *args: P.args, **kwargs: P.kwargs) -> Any:
        """Run the callback."""
        with (self.slot and self.slot()) or nullcontext():
            return self.func(*args, **kwargs) if self.expect_args else self.func()  # type: ignore[call-arg]

    async def await_result(self, result: Awaitable) -> Any:
        """Await the result of the callback."""
        with (self.slot and self.slot()) or nullcontext():
            return await result


class Event(Generic[P]):
    instances: ClassVar[WeakSet[Event]] = WeakSet()

    def __init__(self) -> None:
        """Event

        Events are a powerful tool distribute information between different parts of your code,
        especially from long-living objects like data models to the short-living UI.

        Handlers can be synchronous or asynchronous.
        They can also take arguments if the event contains arguments.

        *Added in version 3.0.0*
        """
        self.callbacks: list[Callback[P]] = []
        self.instances.add(self)

    def subscribe(self, callback: Callable[P, Any] | Callable[[], Any], *,
                  unsubscribe_on_delete: bool | None = None) -> None:
        """Subscribe to the event.

        The ``unsubscribe_on_delete`` can be used to explicitly define
        whether the callback should be automatically unsubscribed when the current client is deleted.
        By default, the callback is automatically unsubscribed if subscribed from within a UI context
        to prevent memory leaks.

        :param callback: the callback which will be called when the event is fired
        :param unsubscribe_on_delete: whether to unsubscribe the callback when the current client is deleted
            (default: ``None`` meaning the callback is automatically unsubscribed if subscribed from within a UI context)
        """
        frame = inspect.currentframe()
        assert frame is not None
        frame = frame.f_back
        assert frame is not None
        callback_ = Callback[P](
            func=callback,
            expect_args=helpers.expects_arguments(callback) or (
                isinstance(getattr(callback, '__self__', None), Event) and
                getattr(callback, '__name__', None) in {'emit', 'call'}
            ),
            filepath=frame.f_code.co_filename,
            line=frame.f_lineno,
        )
        client: Client | None = None
        if Slot.get_stack():  # NOTE: additional check before accessing `context.slot` which would enter script mode
            callback_.slot = weakref.ref(context.slot)
            client = context.client
        if callback_.slot is None and unsubscribe_on_delete is True:
            raise RuntimeError('Calling `subscribe` with `unsubscribe_on_delete=True` outside of a UI context '
                               'is not supported.')
        if client is not None and unsubscribe_on_delete is not False and not core.is_script_mode_preflight():
            client.on_delete(lambda: self.unsubscribe(callback))
        self.callbacks.append(callback_)

    def unsubscribe(self, callback: Callable[P, Any] | Callable[[], Any]) -> None:
        """Unsubscribe a callback from the event.

        :param callback: the callback to unsubscribe from the event
        """
        self.callbacks[:] = [c for c in self.callbacks if c.func != callback]

    def emit(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """Fire the event without waiting for the subscribed callbacks to complete."""
        for callback in self.callbacks:
            _invoke_and_forget(callback, *args, **kwargs)

    async def call(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """Fire the event and wait asynchronously until all subscribed callbacks are completed."""
        await asyncio.gather(*[_invoke_and_await(callback, *args, **kwargs) for callback in self.callbacks])

    async def emitted(self, timeout: float | None = None) -> Any:
        """Wait for an event to be fired and return its arguments.

        :param timeout: the maximum time to wait for the event to be fired (default: ``None`` meaning no timeout)
        """
        future: asyncio.Future[Any] = asyncio.Future()

        def callback(*args: P.args, **kwargs: P.kwargs) -> None:  # pylint: disable=unused-argument
            if not future.done():
                future.set_result(args[0] if len(args) == 1 else args if args else None)

        self.subscribe(callback)
        try:
            return await asyncio.wait_for(future, timeout)
        except TimeoutError as error:
            raise TimeoutError(f'Timed out waiting for event after {timeout} seconds') from error
        finally:
            self.unsubscribe(callback)

    def __await__(self):
        return self.emitted().__await__()


def _invoke_and_forget(callback: Callback[P], *args: P.args, **kwargs: P.kwargs) -> Any:
    try:
        result = callback.run(*args, **kwargs)
        if helpers.should_await(result):
            background_tasks.create_or_defer(
                callback.await_result(result), name=f'{callback.filepath}:{callback.line}')
    except Exception as e:
        core.app.handle_exception(e)


async def _invoke_and_await(callback: Callback[P], *args: P.args, **kwargs: P.kwargs) -> Any:
    result = callback.run(*args, **kwargs)
    if helpers.should_await(result):
        result = await callback.await_result(result)
    return result


def reset() -> None:
    """Reset the event system. (Useful for testing.)"""
    for event in Event.instances:
        event.callbacks.clear()
    Event.instances.clear()
