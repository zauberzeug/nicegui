from __future__ import annotations

import asyncio
import inspect
import weakref
from collections.abc import Awaitable, Callable
from contextlib import nullcontext
from dataclasses import dataclass
from typing import Any, ClassVar, Generic

from typing_extensions import ParamSpec

from . import background_tasks, core, helpers
from .awaitable_response import AwaitableResponse
from .context import context
from .dataclasses import KWONLY_SLOTS
from .logging import log
from .slot import Slot


@dataclass(**KWONLY_SLOTS)
class Callback:
    func: Callable
    filepath: str
    line: int
    slot: weakref.ref[Slot] | None = None

    def run(self, *args: P.args, **kwargs: P.kwargs) -> Any:
        """Run the callback."""
        with (self.slot and self.slot()) or nullcontext():
            return self.func(*args, **kwargs) if helpers.expects_arguments(self.func) else self.func()

    async def await_result(self, result: Awaitable | AwaitableResponse | asyncio.Task) -> Any:
        """Await the result of the callback."""
        with (self.slot and self.slot()) or nullcontext():
            return await result


P = ParamSpec('P')


class Event(Generic[P]):
    instances: ClassVar[list[Event]] = []

    def __init__(self) -> None:
        self.callbacks: list[Callback] = []
        self.instances.append(self)

    def subscribe(self, callback: Callable[P, Any] | Callable[[], Any]) -> None:
        """Subscribe to the event.

        Note that the callback should not be used to update UI since it would probably cause a memory leak.
        Use the ``subscribe_ui`` method instead.

        :param callback: the callback which will be called when the event is fired
        """
        frame = inspect.currentframe()
        assert frame is not None
        frame = frame.f_back
        assert frame is not None
        self.callbacks.append(Callback(func=callback, filepath=frame.f_code.co_filename, line=frame.f_lineno))

    def subscribe_ui(self, callback: Callable[P, Any] | Callable[[], Any]) -> None:
        """Subscribe to the event and automatically unsubscribe when the client disconnects.

        This method is particularly useful for UI callbacks since it cleans up unused references to the callback
        which would otherwise cause a memory leak.

        :param callback: the callback which will be called when the event is fired
        """
        self.subscribe(callback)
        try:
            self.callbacks[-1].slot = weakref.ref(context.slot)
        except RuntimeError as e:
            raise RuntimeError('Calling `subscribe_ui` outside of a UI context is not supported.') from e
        client = context.client

        async def register_disconnect() -> None:
            try:
                await client.connected(timeout=10.0)
                client.on_disconnect(lambda: self.unsubscribe(callback))
            except TimeoutError:
                log.warning('Could not register a disconnect handler for callback %s', callback)
                self.unsubscribe(callback)
        if core.loop and core.loop.is_running():
            background_tasks.create(register_disconnect())
        else:
            core.app.on_startup(register_disconnect())

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


def _invoke_and_forget(callback: Callback, *args: P.args, **kwargs: P.kwargs) -> Any:
    try:
        result = callback.run(*args, **kwargs)
        if _should_await(result):
            if core.loop and core.loop.is_running():
                background_tasks.create(callback.await_result(result), name=f'{callback.filepath}:{callback.line}')
            else:
                core.app.on_startup(callback.await_result(result))
    except Exception:
        log.exception('Could not emit callback %s', callback)


async def _invoke_and_await(callback: Callback, *args: P.args, **kwargs: P.kwargs) -> Any:
    try:
        result = callback.run(*args, **kwargs)
        if _should_await(result):
            result = await callback.await_result(result)
        return result
    except Exception as e:
        core.app.handle_exception(e)


def _should_await(result: Any) -> bool:
    """Determine if a result should be awaited.

    Note: We want to await an awaitable result even if the handler is not a coroutine (like a lambda statement).
    """
    return isinstance(result, Awaitable) and not isinstance(result, AwaitableResponse) and not isinstance(result, asyncio.Task)


def reset() -> None:
    """Reset the event system. (Useful for testing.)"""
    for event in Event.instances:
        event.callbacks.clear()
    Event.instances.clear()
