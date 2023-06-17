from typing import Any, Callable, Optional

from nicegui import ui

from .color_picker import ColorPicker
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class ColorInput(ValueElement, DisableableElement):
    LOOPBACK = False

    def __init__(self,
                 label: Optional[str] = None, *,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 on_change: Optional[Callable[..., Any]] = None,
                 ) -> None:
        """Color Input

        :param label: displayed label for the color input
        :param placeholder: text to show if no color is selected
        :param value: the current color value
        :param on_change: callback to execute when the value changes
        """
        super().__init__(tag='q-input', value=value, on_value_change=on_change)
        if label is not None:
            self._props['label'] = label
        if placeholder is not None:
            self._props['placeholder'] = placeholder

        with self.add_slot('append'):
            self.picker = ColorPicker(on_pick=lambda e: self.set_value(e.color))
            self.button = ui.button(on_click=self.open_picker, icon='colorize') \
                .props('flat round', remove='color').classes('cursor-pointer')

    def open_picker(self) -> None:
        """Open the color picker"""
        if self.value:
            self.picker.set_color(self.value)
        self.picker.open()
