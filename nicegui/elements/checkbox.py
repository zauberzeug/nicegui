from typing import Callable
import justpy as jp
from .bool_element import BoolElement

class Checkbox(BoolElement):

    def __init__(self,
                 text: str = '',
                 value: bool = False,
                 on_change: Callable = None,
                 design: str = '',
                 classes: str = '',
                 ):
        """Checkbox Element

        :param text: the label to display beside the checkbox
        :param value: set to True if initally it should be checked; default is False
        :param design: Quasar props to alter the appearance (see `their reference <https://quasar.dev/vue-components/checkbox>`_)
        :param on_change: callback to execute when value changes
        """
        view = jp.QCheckbox(text=text, input=self.handle_change)

        super().__init__(view, value, on_change, design=design, classes=classes)
