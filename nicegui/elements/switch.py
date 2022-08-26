from typing import Callable, Optional

import justpy as jp

from .bool_element import BoolElement


class Switch(BoolElement):

    def __init__(self, text: str = '', *, value: bool = False, on_change: Optional[Callable] = None):
        """Switch

        :param text: the label to display next to the switch
        :param value: whether it should be active initially (default: `False`)
        :param on_change: callback which is invoked when state is changed by the user
        """
        view = jp.QToggle(text=text, input=self.handle_change, temp=False)

        super().__init__(view, value=value, on_change=on_change)
