from typing import Callable
import justpy as jp
from .bool_element import BoolElement

class Switch(BoolElement):

    def __init__(self,
                 text: str = '',
                 value: bool = False,
                 on_change: Callable = None,
                 design: str = '',
                 classes: str = '',
                 ):
        """Switch Element

        :param text: the label to display next to the switch
        :param value: set to `True` if initally it should be active; default is `False`
        :param design: Quasar props to alter the appearance (see `their reference <https://quasar.dev/vue-components/switch>`_)
        :param on_click: callback which is invoked when state is changed by the user
        """
        view = jp.QToggle(text=text, input=self.handle_change)

        super().__init__(view, value, on_change, design=design, classes=classes)
