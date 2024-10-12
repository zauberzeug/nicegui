from typing import Any, Optional

from ..events import Handler, ValueChangeEventArguments
from .button import Button as button
from .color_picker import ColorPicker as color_picker
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class ColorInput(ValueElement, DisableableElement):
    LOOPBACK = False

    def __init__(self,
                 label: Optional[str] = None, *,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 preview: bool = False,
                 ) -> None:
        """Color Input

        This element extends Quasar's `QInput <https://quasar.dev/vue-components/input>`_ component with a color picker.

        :param label: displayed label for the color input
        :param placeholder: text to show if no color is selected
        :param value: the current color value
        :param on_change: callback to execute when the value changes
        :param preview: change button background to selected color (default: False)
        """
        super().__init__(tag='q-input', value=value, on_value_change=on_change)
        if label is not None:
            self._props['label'] = label
        if placeholder is not None:
            self._props['placeholder'] = placeholder

        with self.add_slot('append'):
            self.picker = color_picker(on_pick=lambda e: self.set_value(e.color))
            self.button = button(on_click=self.open_picker, icon='colorize') \
                .props('flat round', remove='color').classes('cursor-pointer')

        self.preview = preview
        self._update_preview()

    def open_picker(self) -> None:
        """Open the color picker"""
        if self.value:
            self.picker.set_color(self.value)
        self.picker.open()

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        self._update_preview()

    def _update_preview(self) -> None:
        if not self.preview:
            return
        self.button.style(f'''
            background-color: {(self.value or "#fff").split(";", 1)[0]};
            text-shadow: 2px 0 #fff, -2px 0 #fff, 0 2px #fff, 0 -2px #fff, 1px 1px #fff, -1px -1px #fff, 1px -1px #fff, -1px 1px #fff;
        ''')
