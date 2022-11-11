from typing import Callable, Optional

from .value_element import ValueElement


class BoolElement(ValueElement):

    def __init__(self, tag: str, *, value: bool, on_change: Optional[Callable]) -> None:
        super().__init__(tag, value=value, on_change=on_change)
