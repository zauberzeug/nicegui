from typing import Callable
import justpy as jp
from .bool_element import BoolElement

class Checkbox(BoolElement):

    def __init__(self,
                 text: str = '',
                 value: bool = False,
                 design: str = '',
                 on_change: Callable = None):
        """Checkbox Element

        :param text: the label to display beside the checkbox
        :param value: set to True if initally it should be checked; default is False
        :param design: Quasar props to alter the appearance (see `their reference <https://quasar.dev/vue-components/checkbox>`_)
        :param on_change: callback to execute when value changes
        """
        view = jp.QCheckbox(text=text, input=self.handle_change)

        super().__init__(view, design, value, on_change)
