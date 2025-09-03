from __future__ import annotations

import asyncio
import inspect
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Generic, ParamSpec

from . import background_tasks, context, core

startup_coroutines: list[Awaitable] = []
tasks: list[asyncio.Task] = []
log = logging.getLogger('rosys.event')
events: list[Event] = []


@dataclass(slots=True, kw_only=True)
class Callback:
    func: Callable
    filepath: str
    line: int


P = ParamSpec('P')


class Event(Generic[P]):

    def __init__(self) -> None:
        self.callbacks: list[Callback] = []
        events.append(self)

    def subscribe(self, callback: Callable[P, Any]) -> Event[P]:
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
        return self

    def subscribe_ui(self, callback: Callable[P, Any]) -> Event[P]:
        """Subscribe to the event and automatically unsubscribe when the client disconnects.

        This method is particularly useful for UI callbacks since it cleans up unused references to the callback
        which would otherwise cause a memory leak.

        :param callback: the callback which will be called when the event is fired
        """
        self.subscribe(callback)
        client = context.client

        async def register_disconnect() -> None:
            try:
                await client.connected(timeout=10.0)
                client.on_disconnect(lambda: self.unsubscribe(callback))
            except TimeoutError:
                log.warning('Could not register a disconnect handler for callback %s', callback)
                self.unsubscribe(callback)
        background_tasks.create(register_disconnect())
        return self

    def unsubscribe(self, callback: Callable[P, Any]) -> None:
        """Unsubscribe a callback from the event.

        :param callback: the callback to unsubscribe from the event
        """
        self.callbacks[:] = [c for c in self.callbacks if c.func != callback]

    async def call(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """Fire the event and wait asynchronously until all subscribed callbacks are completed."""
        results = asyncio.gather(*[_invoke(callback.func, *args, **kwargs) for callback in self.callbacks],
                                 return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                log.exception('Could not call callback %s', result)

    def emit(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """Fire the event without waiting for the subscribed callbacks to complete."""
        for callback in self.callbacks:
            try:
                result = callback.func(*args, **kwargs)
                if isinstance(result, Awaitable):
                    if core.loop and core.loop.is_running():
                        name = f'{callback.filepath}:{callback.line}'
                        tasks.append(background_tasks.create(result, name=name))
                    else:
                        startup_coroutines.append(result)
            except Exception:
                log.exception('Could not emit callback %s', callback)

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


async def _invoke(handler: Callable[P, Any], *args: P.args, **kwargs: P.kwargs) -> Any:
    result = handler(*args, **kwargs)
    if isinstance(result, Awaitable):
        result = await result
    return result


def reset() -> None:
    """Reset the event system. (Useful for testing.)"""
    for event in events:
        event.callbacks.clear()
    events.clear()
    for task in tasks:
        task.cancel()
    tasks.clear()
    startup_coroutines.clear()
