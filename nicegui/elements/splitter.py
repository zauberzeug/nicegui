from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Splitter(ValueElement, DisableableElement, default_classes='nicegui-splitter'):

    @resolve_defaults
    def __init__(self, *,
                 horizontal: bool | None = DEFAULT_PROP | False,
                 reverse: bool | None = DEFAULT_PROP | False,
                 limits: tuple[float, float] | None = DEFAULT_PROP | (0, 100),
                 value: float | None = DEFAULT_PROPS['model-value'] | 50,
                 on_change: Handler[ValueChangeEventArguments] | None = None,
                 ) -> None:
        """Splitter

        The `ui.splitter` element divides the screen space into resizable sections,
        allowing for flexible and responsive layouts in your application.

        Based on Quasar's Splitter component:
        `Splitter <https://quasar.dev/vue-components/splitter>`_

        It provides three customizable slots, ``before``, ``after``, and ``separator``,
        which can be used to embed other elements within the splitter.

        :param horizontal: Whether to split horizontally instead of vertically
        :param limits: Two numbers representing the minimum and maximum split size of the two panels
        :param value: Size of the first panel (or second if using reverse)
        :param reverse: Whether to apply the model size to the second panel instead of the first
        :param on_change: callback which is invoked when the user releases the splitter
        """
        super().__init__(tag='q-splitter', value=value, on_value_change=on_change, throttle=0.05)
        self._props.set_bool('horizontal', horizontal)
        self._props.set_bool('reverse', reverse)
        self._props.set_optional('limits', limits)

        self.before = self.add_slot('before')
        self.after = self.add_slot('after')
        self.separator = self.add_slot('separator')
