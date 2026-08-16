from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.releasable_element import ReleasableElement


class Slider(ReleasableElement[float | None], DisableableElement):

    @resolve_defaults
    def __init__(self, *,
                 min: float,  # pylint: disable=redefined-builtin
                 max: float,  # pylint: disable=redefined-builtin
                 step: float = DEFAULT_PROP | 1.0,
                 value: float | None = DEFAULT_PROPS['model-value'] | None,
                 on_change: Handler[ValueChangeEventArguments[float | None]] | None = None,
                 on_release: Handler[ValueChangeEventArguments[float | None]] | None = None,
                 ) -> None:
        """Slider

        This element is based on Quasar's `QSlider <https://quasar.dev/vue-components/slider>`_ component.

        :param min: lower bound of the slider
        :param max: upper bound of the slider
        :param step: step size
        :param value: initial value to set position of the slider
        :param on_change: callback to execute when the value changes, including while dragging
        :param on_release: callback to execute when the user releases the slider (*added in version 3.17.0*)
        """
        super().__init__(tag='q-slider', value=value, on_value_change=on_change, throttle=0.05,
                         on_release=on_release)
        self._props['min'] = min
        self._props['max'] = max
        self._props['step'] = step
