import justpy as jp
from typing import Callable
from .element import Element
from ..utils import handle_exceptions, provide_arguments

class Input(Element):

    def __init__(self,
                 placeholder: str = None,
                 value: str = None,
                 on_change: Callable = None):

        view = jp.QInput(placeholder=placeholder, type='text')

        if value is not None:
            view.value = value
        if on_change is not None:
            view.on('change', handle_exceptions(provide_arguments(on_change, 'value')))

        super().__init__(view)
