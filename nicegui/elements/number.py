import justpy as jp
from typing import Callable
from .element import Element
from ..utils import handle_exceptions, provide_arguments

class Number(Element):

    def __init__(self,
                 placeholder: str = None,
                 value: float = None,
                 decimals: int = None,
                 on_change: Callable = None):

        view = jp.QInput(placeholder=placeholder, type='number')

        if value is not None:
            view.value = value if decimals is None else round(value, decimals)
        if on_change is not None:
            view.on('change', handle_exceptions(provide_arguments(on_change, 'value')))

        super().__init__(view)
