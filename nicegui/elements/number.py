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
                 on_change: Callable = None,
                 design: str = '',
                 classes: str='',
                 ):

        view = jp.QInput(
            type='number',
            label=label,
            placeholder=placeholder,
            change=self.handle_change,
        )

        super().__init__(view, value, format, on_change, design=design, classes=classes)

    def handle_change(self, msg):

        msg['value'] = float(msg['value'])

        return super().handle_change(msg)
