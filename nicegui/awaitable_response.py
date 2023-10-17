from __future__ import annotations

from asyncio import Task
from typing import Callable, Optional

from . import background_tasks


class AwaitableResponse:

    def __init__(self, fire_and_forget: Optional[Callable], wait_for_result: Optional[Callable]) -> None:
        """Awaitable Response

        This class can be used to run one of two different callables, depending on whether the response is awaited or not.

        :param fire_and_forget: The callable to run if the response is not awaited.
        :param wait_for_result: The callable to run if the response is awaited.
        """
        self.fire_and_forget_task: Optional[Task] = \
            background_tasks.create(self._start(fire_and_forget), name='fire and forget') if fire_and_forget else None
        self.wait_for_result = wait_for_result

    async def _start(self, command: Callable) -> None:
        command()

    def __await__(self):
        if self.fire_and_forget_task is not None:
            self.fire_and_forget_task.cancel()
        if self.wait_for_result is None:
            raise ValueError('AwaitableResponse has no result to await')
        return self.wait_for_result().__await__()
