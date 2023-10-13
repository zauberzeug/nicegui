from typing import Callable

from . import background_tasks


class AwaitableResponse:

    def __init__(self, fire_and_forget: Callable, wait_for_result: Callable) -> None:
        """Awaitable Response

        This class can be used to run one of two different callables, depending on whether the response is awaited or not.

        :param fire_and_forget: The callable to run if the response is not awaited.
        :param wait_for_result: The callable to run if the response is awaited.
        """
        self.wait_for_result = wait_for_result
        self.fire_and_forget_task = background_tasks.create(self._start(fire_and_forget), name='fire and forget')

    async def _start(self, command: Callable) -> None:
        command()

    def __await__(self):
        self.fire_and_forget_task.cancel()
        return self.wait_for_result().__await__()
