from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any, ClassVar, Concatenate, Generic, TypeVar, cast

from typing_extensions import ParamSpec, Self

from .. import background_tasks, core
from ..awaitable_response import AwaitableResponse
from ..dataclasses import KWONLY_SLOTS
from ..element import Element
from ..helpers import is_coroutine_function

_S = TypeVar('_S')
_T = TypeVar('_T')
_P = ParamSpec('_P')


@dataclass(**KWONLY_SLOTS)
class RefreshableTarget:
    container: RefreshableContainer
    refreshable: refreshable
    instance: Any
    args: tuple[Any, ...]
    kwargs: dict[str, Any]

    current_target: ClassVar[RefreshableTarget | None] = None
    locals: list[Any] = field(default_factory=list)
    next_index: int = 0

    def run(self, func: Callable[..., _T]) -> _T:
        """Run the function and return the result."""
        RefreshableTarget.current_target = self
        self.next_index = 0
        # pylint: disable=no-else-return
        if is_coroutine_function(func):
            async def wait_for_result() -> Any:
                with self.container:
                    if self.instance is None:
                        result = func(*self.args, **self.kwargs)
                    else:
                        result = func(self.instance, *self.args, **self.kwargs)
                    assert isinstance(result, Awaitable)
                    return await result
            return wait_for_result()  # type: ignore
        else:
            with self.container:
                if self.instance is None:
                    return func(*self.args, **self.kwargs)
                else:
                    return func(self.instance, *self.args, **self.kwargs)


class RefreshableContainer(Element, component='refreshable.js'):
    pass


class refreshable(Generic[_P, _T]):

    def __init__(self, func: Callable[_P, _T]) -> None:
        """Refreshable UI functions

        The ``@ui.refreshable`` decorator allows you to create functions that have a ``refresh`` method.
        This method will automatically delete all elements created by the function and recreate them.

        For decorating refreshable methods in classes, there is a ``@ui.refreshable_method`` decorator,
        which is equivalent but prevents static type checking errors.
        """
        self.func = func
        self.instance = None
        self.targets: list[RefreshableTarget] = []

    def __get__(self, instance, _) -> Self:
        self.instance = instance
        return self

    def __getattribute__(self, __name: str) -> Any:
        attribute = object.__getattribute__(self, __name)
        if __name == 'refresh':
            def refresh(*args: Any, _instance=self.instance, **kwargs: Any) -> AwaitableResponse:
                self.instance = _instance
                return attribute(*args, **kwargs)
            return refresh
        return attribute

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _T:
        self.prune()
        target = RefreshableTarget(container=RefreshableContainer(), refreshable=self, instance=self.instance,
                                   args=args, kwargs=kwargs)
        self.targets.append(target)
        return target.run(self.func)

    def refresh(self, *args: Any, **kwargs: Any) -> AwaitableResponse:
        """Refresh the UI elements created by this function.

        This method accepts the same arguments as the function itself or a subset of them.
        It will combine the arguments passed to the function with the arguments passed to this method.

        If the function is awaited, it will wait for all async refresh operations to complete.
        Otherwise, the refresh operations are executed in the background as fire-and-forget tasks.
        """
        self.prune()

        def fire_and_forget() -> None:
            if coroutines := self._execute_refresh(args, kwargs):
                if core.loop and core.loop.is_running():
                    background_tasks.create(asyncio.gather(*coroutines), name=f'refresh {self.func.__name__}')
                else:
                    core.app.on_startup(asyncio.gather(*coroutines))

        async def wait_for_completion() -> None:
            if coroutines := self._execute_refresh(args, kwargs):
                await asyncio.gather(*coroutines)

        return AwaitableResponse(fire_and_forget, wait_for_completion)

    def _execute_refresh(self, args: tuple[Any, ...], kwargs: dict[str, Any]) -> list[Awaitable[Any]]:
        """Execute the refresh and return a list of coroutines for async functions."""
        coroutines: list[Awaitable[Any]] = []
        for target in self.targets:
            if target.instance != self.instance:
                continue
            target.container.clear()
            target.args = args or target.args
            target.kwargs.update(kwargs)
            try:
                result = target.run(self.func)
            except TypeError as e:
                if 'got multiple values for argument' in str(e):
                    function = str(e).split()[0].split('.')[-1]
                    parameter = str(e).split()[-1]
                    raise TypeError(f'{parameter} needs to be consistently passed to {function} '
                                    'either as positional or as keyword argument') from e
                raise
            if is_coroutine_function(self.func):
                assert isinstance(result, Awaitable)
                coroutines.append(result)
        return coroutines

    def prune(self) -> None:
        """Remove all targets that are no longer on a page with a client connection.

        This method is called automatically before each refresh.
        """
        self.targets = [target for target in self.targets if not target.container.is_deleted]


class refreshable_method(Generic[_S, _P, _T], refreshable[_P, _T]):

    def __init__(self, func: Callable[Concatenate[_S, _P], _T]) -> None:
        """Refreshable UI methods

        The `@ui.refreshable_method` decorator allows you to create methods that have a `refresh` method.
        This method will automatically delete all elements created by the function and recreate them.
        """
        super().__init__(func)  # type: ignore


def state(value: Any) -> tuple[Any, Callable[[Any], None]]:
    """Create a state variable that automatically updates its refreshable UI container.

    :param value: The initial value of the state variable.

    :return: A tuple containing the current value and a function to update the value.
    """
    target = cast(RefreshableTarget, RefreshableTarget.current_target)

    try:
        index = target.next_index
    except AttributeError as e:
        raise RuntimeError('ui.state() can only be used inside a @ui.refreshable function') from e

    if index >= len(target.locals):
        target.locals.append(value)
    else:
        value = target.locals[index]

    def set_value(new_value: Any) -> None:
        if target.locals[index] == new_value:
            return
        target.locals[index] = new_value
        target.refreshable.refresh(_instance=target.instance)

    target.next_index += 1

    return value, set_value
