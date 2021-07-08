from typing import Awaitable, Callable, List, Union

startup_tasks: List[Union[Callable, Awaitable]] = []

def on_startup(self, task: Union[Callable, Awaitable]):

    self.startup_tasks.append(task)

shutdown_tasks: List[Union[Callable, Awaitable]] = []

def on_shutdown(self, task: Union[Callable, Awaitable]):

    self.shutdown_tasks.append(task)
