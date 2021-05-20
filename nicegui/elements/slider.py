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
                 on_change: Callable = None,
                 design: str = '',
                 classes: str = '',
                 ):
        """Slider Element

        :param min: lower bound of the slider
        :param max: upper bound of the slider
        :param value: inital value to set position of the slider
        :param design: Quasar props to alter the appearance (see `their reference <https://quasar.dev/vue-components/slider>`_)
        :param on_change: callback which is invoked when the user releases the slider
        """
        view = jp.QSlider(min=min, max=max, step=step, change=self.handle_change)

        super().__init__(view, value, None, on_change, design=design, classes=classes)
