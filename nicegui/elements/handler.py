from typing import Any, Callable, Optional, TypeAlias, TypeVar, Union

EventT = TypeVar('EventT')
Handler: TypeAlias = Optional[Union[Callable[[EventT], Any], Callable[[], Any]]]
