from typing import Any, Callable, Dict, Optional

from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Range(ValueElement, DisableableElement):

    def __init__(self, *,
                 min: float,  # pylint: disable=redefined-builtin
                 max: float,  # pylint: disable=redefined-builtin
                 step: float = 1.0,
                 value: Optional[Dict[str, int]] = None,
                 on_change: Optional[Callable[..., Any]] = None,
                 ) -> None:
        """Range

        This element is based on Quasar's `QRange <https://quasar.dev/vue-components/range>`_ component.

        :param min: lower bound of the range
        :param max: upper bound of the range
        :param step: step size
        :param value: initial value to set min and max position of the range
        :param on_change: callback which is invoked when the user releases the range
        """
        super().__init__(tag='q-range', value=value, on_value_change=on_change, throttle=0.05)
        self._props['min'] = min
        self._props['max'] = max
        self._props['step'] = step
