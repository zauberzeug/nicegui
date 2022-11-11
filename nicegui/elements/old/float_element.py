from typing import Callable, Optional

import justpy as jp

from .value_element import ValueElement


class FloatElement(ValueElement):

    def __init__(self, view: jp.HTMLBaseComponent, *, value: float, format: str = None, on_change: Optional[Callable]):
        self.format = format

        super().__init__(view, value=value, on_change=on_change)

    def value_to_view(self, value: float):
        if value is None:
            return None
        elif self.format is None:
            return str(value)
        else:
            return self.format % float(value)
