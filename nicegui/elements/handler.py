from typing import Any, Callable, TypeVar, Union

from typing_extensions import TypeAlias

EventT = TypeVar('EventT')
Handler: TypeAlias = Union[Callable[[EventT], Any], Callable[[], Any]]
