import justpy as jp
from typing import Awaitable, Callable, Optional, Union
from .value_element import ValueElement

class BoolElement(ValueElement):

    def __init__(self,
                 view: jp.HTMLBaseComponent,
                 *,
                 value: bool,
                 on_change: Optional[Union[Callable, Awaitable]],
                 ):
        super().__init__(view, value=value, on_change=on_change)
