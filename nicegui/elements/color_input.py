from typing import Callable, Optional

import justpy as jp

from .string_element import StringElement


class ColorInput(StringElement):

    def __init__(self, label: str = None, *,
                 placeholder: str = None, value: str = '', on_change: Optional[Callable] = None):
        """Color Input Element

        :param label: displayed label for the color input
        :param placeholder: text to show if no color is selected
        :param value: the current color value
        :param on_change: callback to execute when the input is confirmed by leaving the focus
        """
        view = jp.QInput(
            label=label,
            placeholder=placeholder,
            value=value,
            input=self.handle_change,
            temp=False,
        )

        icon_button = jp.parse_html('''
            <q-icon name="colorize" class="cursor-pointer">
                <q-popup-proxy transition-show="scale" transition-hide="scale" name="popup">
                    <q-color name="color_input"/>
                </q-popup-proxy>
            </q-icon>''')
        view.add_scoped_slot('append', icon_button)
        icon_button.name_dict['color_input'].on('change', self.handle_change)

        super().__init__(view, value=value, on_change=on_change)
