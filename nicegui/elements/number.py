import justpy as jp
from typing import Callable
from .float_element import FloatElement

class Number(FloatElement):

    def __init__(self,
                 label: str = None,
                 *,
                 placeholder: str = None,
                 value: float = None,
                 format: str = None,
                 on_change: Callable = None,
                 ):
        """Number Input Element

        :param label: displayed name for the number input
        :param placeholder: text to show if no value is entered
        :param value: the inital value of the field
        :param format: a string like '%.2f' to format the displayed value
        :param on_change: callback to execute when the input is confirmed by leaving the focus
        """

        view = jp.QInput(
            type='number',
            label=label,
            placeholder=placeholder,
            change=self.handle_change,
        )

        super().__init__(view, value=value, format=format, on_change=on_change)

    def handle_change(self, msg):

        msg['value'] = float(msg['value'])

        return super().handle_change(msg)
