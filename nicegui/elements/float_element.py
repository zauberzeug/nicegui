import justpy as jp
from typing import Callable
from .value_element import ValueElement

class FloatElement(ValueElement):

    def __init__(self, view: jp.HTMLBaseComponent, *, value: float, format: str = None, on_change: Callable):

        self.format = format

        super().__init__(view, value=value, on_change=on_change)

    def set_view_value(self, value: float):

        if value is None:
            self.view.value = None
        elif self.format is None:
            self.view.value = str(value)
        else:
            self.view.value = self.format % float(value)
