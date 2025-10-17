from typing import Optional

from ..events import Handler, ValueChangeEventArguments
from .button import Button as button
from .date import Date as date
from .menu import Menu as menu
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.value_element import ValueElement


class DateInput(LabelElement, ValueElement, DisableableElement):
    LOOPBACK = False

    def __init__(self,
                 label: Optional[str] = None, *,
                 range_input: bool = False,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        """Date Input

        This element extends Quasar's `QInput <https://quasar.dev/vue-components/input>`_ component with a date picker.

        :param label: displayed label for the date input
        :param range_input: if True, allows selecting a range of dates (value will be a dictionary with 'from' and 'to' keys)
        :param placeholder: text to show if no date is selected
        :param value: the current date value
        :param on_change: callback to execute when the value changes
        """
        self.range_input = range_input
        super().__init__(tag='q-input', label=label, value=value, on_value_change=on_change)
        if placeholder is not None:
            self._props['placeholder'] = placeholder

        with self.add_slot('append'):
            with button(on_click=self._sync_value, icon='edit_calendar').props('flat round', remove='color').classes('cursor-pointer') as self.button:
                with menu() as self.menu:
                    self.picker = date(on_change=lambda e: self.set_value(self._dict_to_string(e.value) if self.range_input else e.value)) \
                        .props('no-parent-event', remove='color')
        if self.range_input:
            self.picker.props('range')

    def _dict_to_string(self, value: dict) -> str:
        """Convert a dictionary with 'from' and 'to' keys to a string."""
        if not isinstance(value, dict) or 'from' not in value or 'to' not in value:
            return ''
        return f"{value['from']} - {value['to']}" if value else ''

    def _string_to_dict(self, value: str) -> dict:
        """Convert a string formatted as 'start_date - end_date' to a dictionary."""
        if ' - ' in value:
            from_date, to_date = value.split(' - ')
            return {'from': from_date, 'to': to_date}
        return {}

    def _sync_value(self) -> None:
        """Synchronize the value with the picker."""
        if self.range_input and self.value:
            self.picker.set_value(self._string_to_dict(self.value))
        else:
            self.picker.set_value(self.value or '')
