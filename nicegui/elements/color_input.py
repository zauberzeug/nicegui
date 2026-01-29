import re
from colorsys import rgb_to_yiq
from typing import Any

from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .button import Button as button
from .color_picker import ColorPicker as color_picker
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.value_element import ValueElement

HEX_COLOR_PATTERN_6 = re.compile(r'^#([0-9a-fA-F]{6})$')
HEX_COLOR_PATTERN_3 = re.compile(r'^#([0-9a-fA-F]{3})$')


class ColorInput(LabelElement, ValueElement, DisableableElement):
    LOOPBACK = False

    @resolve_defaults
    def __init__(self,
                 label: str | None = DEFAULT_PROP | None, *,
                 placeholder: str | None = DEFAULT_PROP | None,
                 value: str = DEFAULT_PROPS['model-value'] | '',
                 on_change: Handler[ValueChangeEventArguments] | None = None,
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
        super().__init__(tag='q-input', label=label, value=value, on_value_change=on_change)
        self._props['for'] = self.html_id
        self._props.set_optional('placeholder', placeholder)

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

        color = self.value.strip()
        if HEX_COLOR_PATTERN_6.match(color):
            r = int(color[1:3], 16) / 255
            g = int(color[3:5], 16) / 255
            b = int(color[5:7], 16) / 255
        elif HEX_COLOR_PATTERN_3.match(color):
            r = int(color[1], 16) / 15
            g = int(color[2], 16) / 15
            b = int(color[3], 16) / 15
        else:
            self.button.style('background-color: transparent').props(remove='color')
            return
        luminance = rgb_to_yiq(r, g, b)[0]
        icon_color = 'grey-10' if luminance > 0.5 else 'grey-3'
        self.button.style(f'background-color: {color}').props(f'color="{icon_color}"')
