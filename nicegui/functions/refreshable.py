from typing import Callable, List

from ..element import Element


class refreshable:

    def __init__(self, func: Callable) -> None:
        """Refreshable UI functions

        The `@refreshable` decorator allows you to create functions that have a `refresh` method.
        This method will automatically delete all elements created by the function and recreate them.
        """
        self.func = func
        self.containers: List[Element] = []

    def __call__(self, *args, **kwargs) -> None:
        with Element('div') as container:
            self.func(*args, **kwargs)
        self.containers.append(container)

    def refresh(self) -> None:
        for container in self.containers:
            container.clear()
            with container:
                self.func()
