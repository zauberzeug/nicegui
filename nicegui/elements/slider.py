from typing import Callable
import justpy as jp
from .float_element import FloatElement

class Slider(FloatElement):

    def __init__(self,
                 *,
                 min: float,
                 max: float,
                 value: float = None,
                 step: float = 1,
                 design: str = '',
                 on_change: Callable = None):

        view = jp.QSlider(min=min, max=max, step=step, change=self.handle_change)

        super().__init__(view, design, value, None, on_change)
