from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Slider(ValueElement, DisableableElement):

    @resolve_defaults
    def __init__(self, *,
                 min: float,  # pylint: disable=redefined-builtin
                 max: float,  # pylint: disable=redefined-builtin
                 step: float = DEFAULT_PROP | 1.0,
                 value: float | None = DEFAULT_PROPS['model-value'] | None,
                 on_change: Handler[ValueChangeEventArguments] | None = None,
                 ) -> None:
        """Slider

        This element is based on Quasar's `QSlider <https://quasar.dev/vue-components/slider>`_ component.

        :param min: lower bound of the slider
        :param max: upper bound of the slider
        :param step: step size
        :param value: initial value to set position of the slider
        :param on_change: callback which is invoked when the user releases the slider
        """
        super().__init__(tag='q-slider', value=value, on_value_change=on_change, throttle=0.05)
        self._props['min'] = min
        self._props['max'] = max
        self._props['step'] = step
