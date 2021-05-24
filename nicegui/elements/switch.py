from typing import Callable
import justpy as jp
from .bool_element import BoolElement

class Switch(BoolElement):

    def __init__(self,
                 text: str = '',
                 *,
                 value: bool = False,
                 on_change: Callable = None,
                 ):
        """Switch Element

        :param text: the label to display next to the switch
        :param value: set to `True` if initally it should be active; default is `False`
        :param on_click: callback which is invoked when state is changed by the user
        """
        view = jp.QToggle(text=text, input=self.handle_change)

        super().__init__(view, value=value, on_change=on_change)
