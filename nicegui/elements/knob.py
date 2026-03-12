from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .label import Label
from .mixins.color_elements import TextColorElement
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Knob(ValueElement, DisableableElement, TextColorElement):

    @resolve_defaults
    def __init__(self,
                 value: float = DEFAULT_PROPS['model-value'] | 0.0,
                 *,
                 min: float = DEFAULT_PROP | 0.0,  # pylint: disable=redefined-builtin
                 max: float = DEFAULT_PROP | 1.0,  # pylint: disable=redefined-builtin
                 step: float = DEFAULT_PROP | 0.01,
                 color: str | None = DEFAULT_PROP | 'primary',
                 center_color: str | None = DEFAULT_PROP | None,
                 track_color: str | None = DEFAULT_PROP | None,
                 size: str | None = DEFAULT_PROP | None,
                 show_value: bool = False,
                 on_change: Handler[ValueChangeEventArguments] | None = None,
                 ) -> None:
        """Knob

        This element is based on Quasar's `QKnob <https://quasar.dev/vue-components/knob>`_ component.
        The element is used to take a number input from the user through mouse/touch panning.

        :param value: the initial value (default: 0.0)
        :param min: the minimum value (default: 0.0)
        :param max: the maximum value (default: 1.0)
        :param step: the step size (default: 0.01)
        :param color: knob color (either a Quasar, Tailwind, or CSS color or `None`, default: "primary")
        :param center_color: color name for the center part of the component, examples: primary, teal-10
        :param track_color: color name for the track of the component, examples: primary, teal-10
        :param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl), examples: 16px, 2rem
        :param show_value: whether to show the value as text
        :param on_change: callback to execute when the value changes
        """
        super().__init__(tag='q-knob', value=value, on_value_change=on_change, throttle=0.05, text_color=color)

        self._props['min'] = min
        self._props['max'] = max
        self._props['step'] = step
        self._props['show-value'] = True  # NOTE: enable default slot, e.g. for nested icon
        self._props.set_optional('center-color', center_color)
        self._props.set_optional('track-color', track_color)
        self._props.set_optional('size', size)

        self.label: Label | None = None
        if show_value:
            with self:
                self.label = Label().bind_text_from(self, 'value')
