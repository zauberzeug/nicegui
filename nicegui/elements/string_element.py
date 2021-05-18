import justpy as jp
from typing import Callable
from .value_element import ValueElement

class StringElement(ValueElement):

    def __init__(self,
                 view: jp.HTMLBaseComponent,
                 design: str,
                 value: float,
                 on_change: Callable):

        super().__init__(view, design, value, on_change)
