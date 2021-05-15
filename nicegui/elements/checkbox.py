from typing import Callable
import justpy as jp
from .bool_element import BoolElement

class Checkbox(BoolElement):

    def __init__(self,
                 text: str = '',
                 value: bool = False,
                 design: str = '',
                 on_change: Callable = None):

        view = jp.QCheckbox(text=text, input=self.handle_change)

        super().__init__(view, design, value, on_change)
