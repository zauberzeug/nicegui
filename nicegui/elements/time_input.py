from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .button import Button as button
from .menu import Menu as menu
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.value_element import ValueElement
from .time import Time as time


class TimeInput(LabelElement, ValueElement, DisableableElement):
    LOOPBACK = False

    @resolve_defaults
    def __init__(self,
                 label: str | None = DEFAULT_PROP | None, *,
                 placeholder: str | None = DEFAULT_PROP | None,
                 value: str = DEFAULT_PROPS['model-value'] | '',
                 on_change: Handler[ValueChangeEventArguments] | None = None,
                 ) -> None:
        """Time Input

        This element extends Quasar's `QInput <https://quasar.dev/vue-components/input>`_ component with a time picker.

        *Added in version 3.3.0*

        :param label: displayed label for the time input
        :param placeholder: text to show if no time is selected
        :param value: the current time value
        :param on_change: callback to execute when the value changes
        """
        super().__init__(tag='q-input', label=label, value=value, on_value_change=on_change)
        self._props['for'] = self.html_id
        self._props.set_optional('placeholder', placeholder)

        with self.add_slot('append'):
            with button(icon='schedule', color=None).props('flat round').classes('cursor-pointer') as self.button:
                with menu() as self.menu:
                    self.picker = time()

        self.picker.bind_value(self)
