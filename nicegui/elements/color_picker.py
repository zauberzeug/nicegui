from typing import Callable, Dict

import justpy as jp
from nicegui.events import ColorPickEventArguments, handle_event

from .element import Element


class ColorPicker(Element):

    def __init__(self, *, on_pick: Callable, value: bool = False):
        """Color Picker

        :param on_pick: callback to execute when a color is picked
        :param value: whether the menu is already opened (default: `False`)
        """
        view = jp.parse_html('''
            <q-popup-proxy transition-show="scale" transition-hide="scale" name="popup">
                <q-color name="color_input"/>
            </q-popup-proxy>
            ''')

        def handle_pick(sender, msg: Dict):
            return handle_event(on_pick, ColorPickEventArguments(sender=self, color=msg.value), update=self.parent_view)
        view.name_dict['color_input'].on('change', handle_pick)
        view.name_dict['popup'].value = value

        super().__init__(view)

    def open(self):
        self.view.name_dict['popup'].value = True

    def close(self):
        self.view.name_dict['popup'].value = False
