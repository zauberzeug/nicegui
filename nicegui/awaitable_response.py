from collections.abc import Callable
from inspect import isawaitable

from . import background_tasks, core
from .slot import Slot


class AwaitableResponse:

    def __init__(self, fire_and_forget: Callable | None, wait_for_result: Callable, *, name: str = 'fire') -> None:
        """Awaitable Response

        This class can be used to run one of two different callables, depending on whether the response is awaited or not.
        It must be awaited immediately after creation or not at all.

        If the response is not awaited, nobody could catch exceptions raised by ``fire_and_forget``.
        They are therefore reported to the exception handlers of the client in whose context the response was created,
        in addition to the global exception handlers.

        :param fire_and_forget: The callable to run if the response is not awaited (it may return an awaitable),
            or ``None`` if there is nothing to do in that case (*added in version 4.1.0*)
        :param wait_for_result: The callable to run if the response is awaited.
        :param name: The name of the background task running ``fire_and_forget`` (default: "fire", *added in version 3.18.0*)
        """
        self.fire_and_forget = fire_and_forget
        self.wait_for_result = wait_for_result
        self._is_fired = False
        self._is_awaited = False
        if fire_and_forget is None:
            assert core.loop is not None
            core.loop.call_soon(lambda: setattr(self, '_is_fired', True))  # no task, but a late await still raises
        else:
            stack = Slot.get_stack()  # don't enter script mode by accessing `context.slot_stack`
            background_tasks.create(self._fire(), name=name, context=stack[-1] if stack else None)

    async def _fire(self) -> None:
        if self._is_awaited:
            return
        self._is_fired = True
        assert self.fire_and_forget is not None
        result = self.fire_and_forget()
        if isawaitable(result):
            await result

    def __await__(self):
        if self._is_fired:
            raise RuntimeError('AwaitableResponse must be awaited immediately after creation or not at all')
        self._is_awaited = True
        # NOTE: `Client.run_javascript` relies on `wait_for_result()` starting without a loop step in between,
        # because it adds the request ID to a message that is already in the outbox
        return self.wait_for_result().__await__()


class NullResponse(AwaitableResponse):

    def __init__(self) -> None:  # pylint: disable=super-init-not-called
        """Null Response

        This class can be used to create an AwaitableResponse that does nothing.
        In contrast to AwaitableResponse, it can be created without a running event loop.
        """

    def __await__(self):
        yield from []
