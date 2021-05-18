import justpy as jp
from typing import Callable
from .value_element import ValueElement

class FloatElement(ValueElement):

    def __init__(self,
                 view: jp.HTMLBaseComponent,
                 design: str,
                 value: float,
                 format: str,
                 on_change: Callable):

        self.format = format

        super().__init__(view, design, value, on_change)

    def value_to_view(self, value: float):

        if value is None:
            return None
        elif self.format is None:
            return str(value)
        else:
            return self.format % float(value)
