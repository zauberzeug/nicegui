import justpy as jp
from typing import Awaitable, Callable, Optional, Union
from .value_element import ValueElement

class StringElement(ValueElement):

    def __init__(self,
                 view: jp.HTMLBaseComponent,
                 *,
                 value: float,
                 on_change: Optional[Union[Callable, Awaitable]],
                 ):
        super().__init__(view, value=value, on_change=on_change)
