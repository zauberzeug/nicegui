import justpy as jp
from typing import Callable
from .string_element import StringElement

class Input(StringElement):

    def __init__(self,
                 *,
                 label: str = None,
                 placeholder: str = None,
                 value: str = '',
                 design: str = '',
                 on_change: Callable = None):
        """Text Input Element

        :param label: display name for the text input
        :param placeholder: text to show if no value is entered
        :param value: the current value of the field
        :param design: Quasar props to alter the appearance (see `their reference <https://quasar.dev/vue-components/input>`_)
        :param on_change: callback when the input is confirmed via leaving the focus
        """
        view = jp.QInput(
            label=label,
            placeholder=placeholder,
            value=value,
            change=self.handle_change,
        )

        super().__init__(view, design, value, on_change)
