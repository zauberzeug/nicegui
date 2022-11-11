from typing import Callable, Optional

import justpy as jp

from .value_element import ValueElement


class StringElement(ValueElement):

    def __init__(self, view: jp.HTMLBaseComponent, *, value: float, on_change: Optional[Callable]):
        super().__init__(view, value=value, on_change=on_change)
