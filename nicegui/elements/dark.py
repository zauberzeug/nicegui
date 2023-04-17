from typing import Optional

from ..dependencies import register_component
from .mixins.value_element import ValueElement

register_component('dark', __file__, 'dark.js')


class Dark(ValueElement):
    VALUE_PROP = 'value'

    def __init__(self, value: Optional[bool] = False) -> None:
        super().__init__(tag='dark', value=value, on_value_change=None)

    def turn_on(self) -> None:
        self.value = True

    def turn_off(self) -> None:
        self.value = False

    def auto(self) -> None:
        self.value = None
