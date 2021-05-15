import justpy as jp
from typing import Callable
from .float_element import FloatElement

class Number(FloatElement):

    def __init__(self,
                 *,
                 label: str = None,
                 placeholder: str = None,
                 value: float = None,
                 format: str = None,
                 design: str = '',
                 on_change: Callable = None):

        view = jp.QInput(
            type='number',
            label=label,
            placeholder=placeholder,
            change=self.handle_change,
        )

        super().__init__(view, design, value, format, on_change)

    def handle_change(self, msg):

        msg['value'] = float(msg['value'])

        return super().handle_change(msg)
