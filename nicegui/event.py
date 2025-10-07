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
from .awaitable_response import AwaitableResponse
from .client import Client, ClientConnectionTimeout
from .context import context
from .dataclasses import KWONLY_SLOTS
from .logging import log
from .slot import Slot

P = ParamSpec('P')


@dataclass(**KWONLY_SLOTS)
class Callback(Generic[P]):
    func: Callable[P, Any] | Callable[[], Any]
    filepath: str
    line: int
    slot: weakref.ref[Slot] | None = None

    def run(self, *args: P.args, **kwargs: P.kwargs) -> Any:
        """Run the callback."""
        with (self.slot and self.slot()) or nullcontext():
            expect_args = helpers.expects_arguments(self.func)
            return self.func(*args, **kwargs) if expect_args else self.func()  # type: ignore[call-arg]

    async def await_result(self, result: Awaitable | AwaitableResponse | asyncio.Task) -> Any:
        """Await the result of the callback."""
        with (self.slot and self.slot()) or nullcontext():
            return await result


class Event(Generic[P]):
    instances: ClassVar[WeakSet[Event]] = WeakSet()

    def __init__(self, local: bool = False) -> None:
        """Event

        Events are a powerful tool distribute information between different parts of your code,
        especially from long-living objects like data models to the short-living UI.

        Handlers can be synchronous or asynchronous.
        They can also take arguments if the event contains arguments.

        When distributed mode is enabled via `ui.run(distributed=True)`, events are automatically shared
        across all instances in the network unless `local=True` is specified.

        *Added in version 3.0.0*

        :param local: if True, event will not be distributed even when distributed mode is active (default: False)
        """
        self.callbacks: list[Callback[P]] = []
        self.local = local
        # NOTE: Use creation location for topic to ensure same Event in different processes shares the same topic
        frame = inspect.currentframe()
        assert frame is not None
        frame = frame.f_back
        assert frame is not None
        # NOTE: Skip frames from typing module (when using Event[T]() syntax)
        while frame and 'typing.py' in frame.f_code.co_filename:
            frame = frame.f_back
        assert frame is not None
        self.topic = f'event_{frame.f_code.co_filename}:{frame.f_lineno}'
        self._zenoh_setup_done = False
        self.instances.add(self)
        self._setup_distributed()

    def subscribe(self, callback: Callable[P, Any] | Callable[[], Any], *,
                  unsubscribe_on_disconnect: bool | None = None) -> None:
        """Subscribe to the event.

        The ``unsubscribe_on_disconnect`` can be used to explicitly define
        whether the callback should be automatically unsubscribed when the client disconnects.
        By default, the callback is automatically unsubscribed if subscribed from within a UI context
        to prevent memory leaks.

        :param callback: the callback which will be called when the event is fired
        :param unsubscribe_on_disconnect: whether to unsubscribe the callback when the client disconnects
            (default: ``None`` meaning the callback is automatically unsubscribed if subscribed from within a UI context)
        """
        frame = inspect.currentframe()
        assert frame is not None
        frame = frame.f_back
        assert frame is not None
        callback_ = Callback[P](func=callback, filepath=frame.f_code.co_filename, line=frame.f_lineno)
        client: Client | None = None
        if Slot.get_stack():  # NOTE: additional check before accessing `context.slot` which would enter script mode
            callback_.slot = weakref.ref(context.slot)
            client = context.client
        if callback_.slot is None and unsubscribe_on_disconnect is True:
            raise RuntimeError('Calling `subscribe` with `unsubscribe_on_disconnect=True` outside of a UI context '
                               'is not supported.')
        if client is not None and unsubscribe_on_disconnect is not False and not core.is_script_mode_preflight():
            async def register_disconnect() -> None:
                try:
                    await client.connected()
                    client.on_disconnect(lambda: self.unsubscribe(callback))
                except ClientConnectionTimeout:
                    log.debug('Could not register a disconnect handler for callback %s', callback)
                    self.unsubscribe(callback)
            if core.loop and core.loop.is_running():
                background_tasks.create(register_disconnect())
            else:
                core.app.on_startup(register_disconnect())
        self.callbacks.append(callback_)

    def unsubscribe(self, callback: Callable[P, Any] | Callable[[], Any]) -> None:
        """Unsubscribe a callback from the event.

        :param callback: the callback to unsubscribe from the event
        """
        self.callbacks[:] = [c for c in self.callbacks if c.func != callback]

    def _setup_distributed(self) -> None:
        """Set up distributed event handling if enabled."""
        if self.local or self._zenoh_setup_done:
            return

        from .distributed import DistributedSession
        session = DistributedSession.get()
        if session is None:
            return

        def remote_handler(data: dict) -> None:
            """Handle events received from remote instances."""
            for callback in self.callbacks:
                _invoke_and_forget(callback, *data.get('args', ()), **data.get('kwargs', {}))

        session.subscribe(self.topic, remote_handler)
        self._zenoh_setup_done = True

    def emit(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """Fire the event without waiting for the subscribed callbacks to complete."""
        for callback in self.callbacks:
            _invoke_and_forget(callback, *args, **kwargs)

        if not self.local:
            from .distributed import DistributedSession
            session = DistributedSession.get()
            if session is not None:
                session.publish(self.topic, {'args': args, 'kwargs': kwargs})

    async def call(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """Fire the event and wait asynchronously until all subscribed callbacks are completed."""
        await asyncio.gather(*[_invoke_and_await(callback, *args, **kwargs) for callback in self.callbacks])

        if not self.local:
            from .distributed import DistributedSession
            session = DistributedSession.get()
            if session is not None:
                session.publish(self.topic, {'args': args, 'kwargs': kwargs})

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
        if _should_await(result):
            if core.loop and core.loop.is_running():
                background_tasks.create(callback.await_result(result), name=f'{callback.filepath}:{callback.line}')
            else:
                core.app.on_startup(callback.await_result(result))
    except Exception:
        log.exception('Could not emit callback %s', callback)


async def _invoke_and_await(callback: Callback[P], *args: P.args, **kwargs: P.kwargs) -> Any:
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
