from typing import Callable
import justpy as jp
from .bool_element import BoolElement

class Checkbox(BoolElement):

    def __init__(self,
                 text: str = '',
                 *,
                 value: bool = False,
                 on_change: Callable = None,
                 ):
        """Checkbox Element

        :param text: the label to display next to the checkbox
        :param value: set to `True` if it should be checked initally; default is `False`
        :param on_change: callback to execute when value changes
        """
        view = jp.QCheckbox(text=text, input=self.handle_change)

        super().__init__(view, value=value, on_change=on_change)
