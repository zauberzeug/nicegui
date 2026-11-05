import asyncio
from collections.abc import Callable
from inspect import isawaitable

from . import background_tasks
from .slot import Slot


class AwaitableResponse:

    def __init__(self, fire_and_forget: Callable, wait_for_result: Callable, *, name: str = 'fire') -> None:
        """Awaitable Response

        This class can be used to run one of two different callables, depending on whether the response is awaited or not.
        It must be awaited immediately after creation or not at all.

        If the response is not awaited, nobody could catch exceptions raised by ``fire_and_forget``.
        They are therefore reported to the exception handlers of the client in whose context the response was created,
        in addition to the global exception handlers.

        :param fire_and_forget: The callable to run if the response is not awaited (it may return an awaitable).
        :param wait_for_result: The callable to run if the response is awaited.
        :param name: The name of the background task running ``fire_and_forget`` (default: "fire", *added in version 3.18.0*)
        """
        self.fire_and_forget = fire_and_forget
        self.wait_for_result = wait_for_result
        self._is_fired = False
        self._is_awaited = False
        stack = Slot.get_stack()  # don't enter script mode by accessing `context.slot_stack`
        self._task = background_tasks.create(self._fire(), name=name, context=stack[-1] if stack else None)

    async def _fire(self) -> None:
        if self._is_awaited:
            return
        self._is_fired = True
        result = self.fire_and_forget()
        if isawaitable(result):
            await result

    def __await__(self):
        if self._is_fired:
            raise RuntimeError('AwaitableResponse must be awaited immediately after creation or not at all')
        self._is_awaited = True
        return self._wait_with_ordered_fire().__await__()

    async def _wait_with_ordered_fire(self):
        """Await the result while preserving the order of calls made in Python.

        The fire-and-forget task is scheduled at creation time but has not run
        yet when ``__await__`` starts. Yielding control to the event loop once
        lets previously created responses send their fire-and-forget messages
        first, so the browser executes the calls in the order they were made
        (e.g. `run_method('a'); await run_method('b')`), instead of the awaited
        message overtaking them (#6472).
        """
        if self._task is not None and not self._task.done():
            await asyncio.sleep(0)
        return await self.wait_for_result()


class NullResponse(AwaitableResponse):

    def __init__(self) -> None:  # pylint: disable=super-init-not-called
        """Null Response

        This class can be used to create an AwaitableResponse that does nothing.
        In contrast to AwaitableResponse, it can be created without a running event loop.
        """

    def __await__(self):
        yield from []
