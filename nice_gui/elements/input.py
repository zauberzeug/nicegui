import justpy as jp
from typing import Callable, Literal, Union
from .element import Element
from ..utils import handle_exceptions, provide_arguments

class Input(Element):

    def __init__(self,
                 placeholder: str = None,
                 value: Union[str, float] = None,
                 type: Literal['text', 'number'] = 'text',
                 on_change: Callable = None):

        view = jp.QInput(placeholder=placeholder, type=type)

        if value is not None:
            view.value = value
        if on_change is not None:
            view.on('input', handle_exceptions(provide_arguments(on_change, 'value')))

        super().__init__(view)
