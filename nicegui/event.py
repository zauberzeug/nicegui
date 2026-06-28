from __future__ import annotations

import asyncio
import sys
import weakref
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, ClassVar, Generic
from weakref import WeakSet

from typing_extensions import ParamSpec

from . import background_tasks, core, helpers
from .client import Client
from .helpers.functions import is_unmanaged_awaitable
from .slot import Slot

P = ParamSpec('P')
_EVENT_FORWARDING_METHODS = {'emit', 'call'}


@dataclass(kw_only=True, slots=True)
class Callback(Generic[P]):
    func: Callable[P, Any] | Callable[[], Any]
    expect_args: bool
    filepath: str
    line: int
    slot: weakref.ref[Slot] | None = None

    def run(self, *args: P.args, **kwargs: P.kwargs) -> Any:
        """Run the callback."""
        func = self.func
        expect_args = self.expect_args
        slot_ref = self.slot
        if slot_ref is None:
            return func(*args, **kwargs) if expect_args else func()  # type: ignore[call-arg]
        slot = slot_ref()
        if slot is None:
            return func(*args, **kwargs) if expect_args else func()  # type: ignore[call-arg]
        _, stack = Slot._get_or_create_stack()  # pylint: disable=protected-access
        stack.append(slot)
        try:
            return func(*args, **kwargs) if expect_args else func()  # type: ignore[call-arg]
        finally:
            stack.pop()

    async def await_result(self, awaitable: Awaitable) -> Any:
        """Await the result of the callback."""
        slot_ref = self.slot
        if slot_ref is None:
            return await awaitable
        slot = slot_ref()
        if slot is None:
            return await awaitable
        _, stack = Slot._get_or_create_stack()  # pylint: disable=protected-access
        stack.append(slot)
        try:
            return await awaitable
        finally:
            stack.pop()


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
                  expect_args: bool | None = None,
                  unsubscribe_on_delete: bool | None = None) -> None:
        """Subscribe to the event.

        The ``unsubscribe_on_delete`` can be used to explicitly define
        whether the callback should be automatically unsubscribed when the current client is deleted.
        By default, the callback is automatically unsubscribed if subscribed from within a UI context
        to prevent memory leaks.

        :param callback: the callback which will be called when the event is fired
        :param expect_args: whether to forward the event's arguments to the callback
            (default: ``None`` meaning auto-detected from the callback's signature, *added in version 3.13.0*)
        :param unsubscribe_on_delete: whether to unsubscribe the callback when the current client is deleted
            (default: ``None`` meaning the callback is automatically unsubscribed if subscribed from within a UI context)
        """
        frame = sys._getframe(1)  # pylint: disable=protected-access
        callback_entry = Callback[P](
            func=callback,
            expect_args=_should_forward_event_args(callback, expect_args),
            filepath=frame.f_code.co_filename,
            line=frame.f_lineno,
        )
        client: Client | None = None
        slot_stack = Slot.peek_stack()  # avoids creating a slot stack when there is no UI context
        if slot_stack:
            slot = slot_stack[-1]
            callback_entry.slot = weakref.ref(slot)
            client = slot.parent.client
        if callback_entry.slot is None and unsubscribe_on_delete is True:
            raise RuntimeError('Calling `subscribe` with `unsubscribe_on_delete=True` outside of a UI context '
                               'is not supported.')
        if client is not None and unsubscribe_on_delete is not False and not core.is_script_mode_preflight():
            client.on_delete(lambda: self.unsubscribe(callback))
        self.callbacks.append(callback_entry)

    def unsubscribe(self, callback: Callable[P, Any] | Callable[[], Any]) -> None:
        """Unsubscribe a callback from the event.

        :param callback: the callback to unsubscribe from the event
        """
        self.callbacks[:] = [c for c in self.callbacks if c.func != callback]

    def emit(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """Fire the event without waiting for the subscribed callbacks to complete."""
        # A synchronous emit runs in one task; resolve its slot stack once for all callbacks.
        slot_stack: list[Slot] | None = None
        for callback in self.callbacks:
            try:
                expect_args = callback.expect_args
                func = callback.func
                slot_ref = callback.slot
                slot = slot_ref() if slot_ref is not None else None
                if slot is not None:
                    if slot_stack is None:
                        _, slot_stack = Slot._get_or_create_stack()  # pylint: disable=protected-access
                    slot_stack.append(slot)
                    try:
                        result = func(*args, **kwargs) if expect_args else func()  # type: ignore[call-arg]
                    finally:
                        slot_stack.pop()
                elif expect_args:
                    result = func(*args, **kwargs)
                else:
                    result = func()  # type: ignore[call-arg]
                if is_unmanaged_awaitable(result):
                    name = f'{callback.filepath}:{callback.line}'
                    background_tasks.create_or_defer(callback.await_result(result), name=name)
            except Exception as e:
                core.app.handle_exception(e)

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

        self.subscribe(callback, expect_args=True)
        try:
            return await asyncio.wait_for(future, timeout)
        except TimeoutError as error:
            raise TimeoutError(f'Timed out waiting for event after {timeout} seconds') from error
        finally:
            self.unsubscribe(callback)

    def __await__(self):
        return self.emitted().__await__()


async def _invoke_and_await(callback: Callback[P], *args: P.args, **kwargs: P.kwargs) -> Any:
    result = callback.run(*args, **kwargs)
    if is_unmanaged_awaitable(result):
        result = await callback.await_result(result)
    return result


def _should_forward_event_args(callback: Callable[P, Any] | Callable[[], Any], expect_args: bool | None) -> bool:
    if expect_args is not None:
        return expect_args
    if helpers.expects_arguments(callback):
        return True
    # Event.emit/call accept *args, so signature inspection alone cannot tell they forward payloads.
    return (
        isinstance(getattr(callback, '__self__', None), Event)
        and getattr(callback, '__name__', None) in _EVENT_FORWARDING_METHODS
    )


def reset() -> None:
    """Reset the event system. (Useful for testing.)"""
    for event in Event.instances:
        event.callbacks.clear()
    Event.instances.clear()
