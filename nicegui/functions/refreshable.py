from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, List, Tuple, Union

from typing_extensions import Self

from .. import background_tasks, globals
from ..element import Element
from ..helpers import KWONLY_SLOTS, is_coroutine_function


@dataclass(**KWONLY_SLOTS)
class RefreshableTarget:
    container: Element
    instance: Any
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]

    def run(self, func: Callable[..., Any]) -> Union[None, Awaitable]:
        if is_coroutine_function(func):
            async def wait_for_result() -> None:
                with self.container:
                    if self.instance is None:
                        await func(*self.args, **self.kwargs)
                    else:
                        await func(self.instance, *self.args, **self.kwargs)
            return wait_for_result()
        else:
            with self.container:
                if self.instance is None:
                    func(*self.args, **self.kwargs)
                else:
                    func(self.instance, *self.args, **self.kwargs)
            return None  # required by mypy


class RefreshableContainer(Element, component='refreshable.js'):
    pass


class refreshable:

    def __init__(self, func: Callable[..., Any]) -> None:
        """Refreshable UI functions

        The `@ui.refreshable` decorator allows you to create functions that have a `refresh` method.
        This method will automatically delete all elements created by the function and recreate them.
        """
        self.func = func
        self.instance = None
        self.targets: List[RefreshableTarget] = []

    def __get__(self, instance, _) -> Self:
        self.instance = instance
        return self

    def __call__(self, *args: Any, **kwargs: Any) -> Union[None, Awaitable]:
        self.prune()
        target = RefreshableTarget(container=RefreshableContainer(), instance=self.instance, args=args, kwargs=kwargs)
        self.targets.append(target)
        return target.run(self.func)

    def refresh(self, *args: Any, **kwargs: Any) -> None:
        self.prune()
        for target in self.targets:
            if target.instance != self.instance:
                continue
            target.container.clear()
            target.args = args or target.args
            target.kwargs.update(kwargs)
            result = target.run(self.func)
            if is_coroutine_function(self.func):
                assert result is not None
                if globals.loop and globals.loop.is_running():
                    background_tasks.create(result)
                else:
                    globals.app.on_startup(result)

    def prune(self) -> None:
        self.targets = [target for target in self.targets if target.container.client.id in globals.clients]
