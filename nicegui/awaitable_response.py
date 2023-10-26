from __future__ import annotations

from typing import Callable

from . import background_tasks


class AwaitableResponse:

    def __init__(self, fire_and_forget: Callable, wait_for_result: Callable) -> None:
        """Awaitable Response

        This class can be used to run one of two different callables, depending on whether the response is awaited or not.
        It must be awaited immediately after creation or not at all.

        :param fire_and_forget: The callable to run if the response is not awaited.
        :param wait_for_result: The callable to run if the response is awaited.
        """
        self.fire_and_forget = fire_and_forget
        self.wait_for_result = wait_for_result
        self._is_fired = False
        self._is_awaited = False
        background_tasks.create(self._fire(), name='fire')

    async def _fire(self) -> None:
        if self._is_awaited:
            return
        self._is_fired = True
        self.fire_and_forget()

    def __await__(self):
        if self._is_fired:
            raise RuntimeError('AwaitableResponse must be awaited immediately after creation or not at all')
        self._is_awaited = True
        return self.wait_for_result().__await__()


class NullResponse(AwaitableResponse):

    def __init__(self) -> None:  # pylint: disable=super-init-not-called
        """Null Response

        This class can be used to create an AwaitableResponse that does nothing.
        In contrast to AwaitableResponse, it can be created without a running event loop.
        """

    def __await__(self):
        yield from []
