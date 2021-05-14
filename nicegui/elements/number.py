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
            **{key: True for key in design.split()},
            change=self.handle_change,
        )

        super().__init__(view, value=value, format=format, on_change=on_change)
