from typing import Callable, List

from typing_extensions import Self

from ..dependencies import register_component
from ..element import Element

register_component('refreshable', __file__, 'refreshable.js')


class refreshable:

    def __init__(self, func: Callable) -> None:
        """Refreshable UI functions

        The `@ui.refreshable` decorator allows you to create functions that have a `refresh` method.
        This method will automatically delete all elements created by the function and recreate them.
        """
        self.func = func
        self.instance = None
        self.containers: List[Element] = []

    def __get__(self, instance, _) -> Self:
        self.instance = instance
        return self

    def __call__(self) -> None:
        with Element('refreshable') as container:
            self.func() if self.instance is None else self.func(self.instance)
        self.containers.append(container)

    def refresh(self) -> None:
        for container in self.containers:
            container.clear()
            with container:
                self.func() if self.instance is None else self.func(self.instance)
