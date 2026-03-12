from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Time(ValueElement, DisableableElement):

    @resolve_defaults
    def __init__(self,
                 value: str | None = DEFAULT_PROPS['model-value'] | None, *,
                 mask: str = DEFAULT_PROP | 'HH:mm',
                 on_change: Handler[ValueChangeEventArguments] | None = None,
                 ) -> None:
        """Time Picker

        This element is based on Quasar's `QTime <https://quasar.dev/vue-components/time>`_ component.
        The time is a string in the format defined by the `mask` parameter.

        :param value: the initial time
        :param mask: the format of the time string (default: 'HH:mm')
        :param on_change: callback to execute when changing the time
        """
        super().__init__(tag='q-time', value=value, on_value_change=on_change)
        self._props['mask'] = mask
