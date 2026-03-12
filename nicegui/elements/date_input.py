from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .button import Button as button
from .date import Date as date
from .menu import Menu as menu
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.value_element import ValueElement


class DateInput(LabelElement, ValueElement, DisableableElement):
    LOOPBACK = False

    @resolve_defaults
    def __init__(self,
                 label: str | None = DEFAULT_PROP | None, *,
                 range_input: bool = False,
                 placeholder: str | None = DEFAULT_PROP | None,
                 value: str = DEFAULT_PROPS['model-value'] | '',
                 on_change: Handler[ValueChangeEventArguments] | None = None,
                 ) -> None:
        """Date Input

        This element extends Quasar's `QInput <https://quasar.dev/vue-components/input>`_ component with a date picker.

        *Added in version 3.3.0*

        :param label: displayed label for the date input
        :param range_input: if True, allows selecting a range of dates (value will be a dictionary with "from" and "to" keys)
        :param placeholder: text to show if no date is selected
        :param value: the current date value
        :param on_change: callback to execute when the value changes
        """
        self._range_input = range_input
        super().__init__(tag='q-input', label=label, value=value, on_value_change=on_change)
        self._props['for'] = self.html_id
        self._props.set_optional('placeholder', placeholder)

        with self.add_slot('append'):
            with button(icon='edit_calendar', color=None).props('flat round').classes('cursor-pointer') as self.button:
                with menu() as self.menu:
                    self.picker = date().props('no-parent-event').props('range' if range_input else '')

        self.picker.bind_value(self,
                               forward=lambda v: self._picker_to_input_value(v) if self._range_input else v,
                               backward=lambda v: self._input_to_picker_value(v) if self._range_input else v)

    def _picker_to_input_value(self, value: dict | str) -> str | None:
        if isinstance(value, dict):
            return f'{value["from"]} - {value["to"]}' if 'from' in value and 'to' in value else None
        else:
            return value

    def _input_to_picker_value(self, value: str | None) -> dict | str | None:
        if value and ' - ' in value:
            from_date, to_date = value.split(' - ', 1)
            return {'from': from_date, 'to': to_date}
        else:
            return value
