from typing import Callable
import justpy as jp
from .element import Element
from ..utils import handle_exceptions, provide_arguments

class Slider(Element):

    def __init__(self, min: float, max: float, on_change: Callable = None):

        view = jp.QSlider(min=min, max=max)

        if on_change is not None:
            view.on('input', handle_exceptions(provide_arguments(on_change, 'value')))

        super().__init__(view)
