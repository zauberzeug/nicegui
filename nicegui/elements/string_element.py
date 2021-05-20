import justpy as jp
from typing import Callable
from .value_element import ValueElement

class StringElement(ValueElement):

    def __init__(self,
                 view: jp.HTMLBaseComponent,
                 value: float,
                 on_change: Callable,
                 design: str,
                 classes: str,
                 ):

        super().__init__(view, value, on_change, design, classes)
