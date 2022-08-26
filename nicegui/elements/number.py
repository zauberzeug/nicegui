from typing import Callable, Dict, Optional

import justpy as jp

from .float_element import FloatElement


class Number(FloatElement):

    def __init__(
            self, label: str = None, *,
            placeholder: str = None, value: float = None, format: str = None, on_change: Optional[Callable] = None):
        """Number Input

        :param label: displayed name for the number input
        :param placeholder: text to show if no value is entered
        :param value: the initial value of the field
        :param format: a string like '%.2f' to format the displayed value
        :param on_change: callback to execute when the input is confirmed by leaving the focus
        """
        view = jp.QInput(
            type='number',
            label=label,
            placeholder=placeholder,
            change=self.handle_change,
            disable_input_event=True,
            temp=False,
        )

        super().__init__(view, value=value, format=format, on_change=on_change)

    def handle_change(self, msg: Dict):
        msg['value'] = float(msg['value'])

        return super().handle_change(msg)
