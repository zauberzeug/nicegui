from typing import Callable, Optional

import justpy as jp

from .string_element import StringElement


class ColorInput(StringElement):

    def __init__(self, label: str = None, *,
                 placeholder: str = None, value: str = '', on_change: Optional[Callable] = None):
        """Color Input

        :param label: displayed label for the color input
        :param placeholder: text to show if no color is selected
        :param value: the current color value
        :param on_change: callback to execute when the input is confirmed by leaving the focus
        """
        view = jp.QInput(
            label=label,
            placeholder=placeholder,
            value=value,
            change=self.handle_change,
            disable_input_event=True,
            temp=False,
        )

        self._icon_button = jp.parse_html('''
            <q-icon name="colorize" class="cursor-pointer">
                <q-popup-proxy transition-show="scale" transition-hide="scale" name="popup" no-parent-event>
                    <q-color name="color_input"/>
                </q-popup-proxy>
            </q-icon>''')
        view.add_scoped_slot('append', self._icon_button)
        self._icon_button.on('click', lambda *_: self.open() or False)
        self._icon_button.name_dict['color_input'].on('change', self.handle_change)
        self._icon_button.name_dict['color_input'].disable_input_event = True
        self._icon_button.name_dict['popup'].on('input', lambda *_: self.update() or False)
        self._icon_button.name_dict['popup'].on('show', lambda *_: self.update() or False)
        self._icon_button.name_dict['popup'].on('hide', lambda *_: self.update() or False)

        super().__init__(view, value=value, on_change=on_change)

    def open(self):
        self._icon_button.name_dict['popup'].value = True
        self.update()

    def close(self):
        self.view.name_dict['popup'].value = False
        self.update()
