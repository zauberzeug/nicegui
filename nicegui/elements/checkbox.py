from typing import Callable
import justpy as jp
from .bool_element import BoolElement

class Checkbox(BoolElement):

    def __init__(self, text: str = '', value: bool = False, on_change: Callable = None):

        view = jp.QCheckbox(text=text, input=self.handle_change)

        super().__init__(view, value=value, on_change=on_change)
