from typing import Optional

from ..dependencies import register_component
from .mixins.value_element import ValueElement

register_component('dark_mode', __file__, 'dark_mode.js')


class DarkMode(ValueElement):
    VALUE_PROP = 'value'

    def __init__(self, value: Optional[bool] = False) -> None:
        super().__init__(tag='dark_mode', value=value, on_value_change=None)

    def enable(self) -> None:
        self.value = True

    def disable(self) -> None:
        self.value = False

    def toggle(self) -> None:
        if self.value is None:
            raise ValueError('Cannot toggle dark mode when it is set to auto.')
        self.value = not self.value

    def auto(self) -> None:
        self.value = None
