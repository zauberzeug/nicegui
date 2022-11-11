from typing import Callable, Optional

import justpy as jp

from .bool_element import BoolElement


class Checkbox(BoolElement):

    def __init__(self, text: str = '', *, value: bool = False, on_change: Optional[Callable] = None):
        """Checkbox

        :param text: the label to display next to the checkbox
        :param value: whether it should be checked initially (default: `False`)
        :param on_change: callback to execute when value changes
        """
        view = jp.QCheckbox(text=text, input=self.handle_change, temp=False)

        super().__init__(view, value=value, on_change=on_change)
