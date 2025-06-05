from typing import Optional

from ..events import Handler, ValueChangeEventArguments
from .button import Button as button
from .menu import Menu as menu
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.value_element import ValueElement
from .time import Time as time


class TimeInput(LabelElement, ValueElement, DisableableElement):
    LOOPBACK = False

    def __init__(self,
                 label: Optional[str] = None, *,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        """Time Input

        This element extends Quasar's `QInput <https://quasar.dev/vue-components/input>`_ component with a time picker.

        :param label: displayed label for the time input
        :param placeholder: text to show if no time is selected
        :param value: the current time value
        :param on_change: callback to execute when the value changes
        """
        super().__init__(tag='q-input', label=label, value=value, on_value_change=on_change)
        if placeholder is not None:
            self._props['placeholder'] = placeholder

        with self.add_slot('append'):
            with button(on_click=self._sync_value, icon='schedule').props('flat round', remove='color').classes('cursor-pointer') as self.button:
                with menu() as self.menu:
                    self.picker = time(on_change=lambda e: self.set_value(e.value))

    def _sync_value(self) -> None:
        """Synchronize the value with the picker."""
        if self.value:
            self.picker.set_value(self.value)
        else:
            self.picker.set_value('')
