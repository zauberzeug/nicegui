from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Range(ValueElement, DisableableElement):

    @resolve_defaults
    def __init__(self, *,
                 min: float,  # pylint: disable=redefined-builtin
                 max: float,  # pylint: disable=redefined-builtin
                 step: float = DEFAULT_PROP | 1.0,
                 value: dict[str, float] | None = DEFAULT_PROPS['model-value'] | None,
                 on_change: Handler[ValueChangeEventArguments] | None = None,
                 ) -> None:
        """Range

        This element is based on Quasar's `QRange <https://quasar.dev/vue-components/range>`_ component.

        :param min: lower bound of the range
        :param max: upper bound of the range
        :param step: step size
        :param value: initial value to set min and max position of the range (default: ``min`` to ``max``)
        :param on_change: callback which is invoked when the user releases the range
        """
        super().__init__(tag='q-range', value=value or {'min': min, 'max': max},
                         on_value_change=on_change, throttle=0.05)
        self._props['min'] = min
        self._props['max'] = max
        self._props['step'] = step

    @property
    def min(self) -> float:
        """The minimum value allowed."""
        return self._props['min']

    @min.setter
    def min(self, value: float) -> None:
        if self._props['min'] == value:
            return
        self._props['min'] = value

    @property
    def max(self) -> float:
        """The maximum value allowed."""
        return self._props['max']

    @max.setter
    def max(self, value: float) -> None:
        if self._props['max'] == value:
            return
        self._props['max'] = value

    @property
    def step(self) -> float:
        """The step size between valid values."""
        return self._props['step']

    @step.setter
    def step(self, value: float) -> None:
        if self._props['step'] == value:
            return
        self._props['step'] = value
