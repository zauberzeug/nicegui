from typing import Callable, Optional

import justpy as jp

from .float_element import FloatElement


class Slider(FloatElement):

    def __init__(self, *,
                 min: float,
                 max: float,
                 step: float = 1,
                 value: float = None,
                 on_change: Optional[Callable] = None):
        """Slider

        :param min: lower bound of the slider
        :param max: upper bound of the slider
        :param step: step size
        :param value: initial value to set position of the slider
        :param on_change: callback which is invoked when the user releases the slider
        """
        view = jp.QSlider(min=min, max=max, step=step, change=self.handle_change, disable_input_event=True, temp=False)

        super().__init__(view, value=value, on_change=on_change)
