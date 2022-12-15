from typing import Callable, Dict

from nicegui.events import ColorPickEventArguments, handle_event

from ..element import Element
from .menu import Menu


class ColorPicker(Menu):

    def __init__(self, *, on_pick: Callable, value: bool = False) -> None:
        """Color Picker

        :param on_pick: callback to execute when a color is picked
        :param value: whether the menu is already opened (default: `False`)
        """
        super().__init__(value=value)
        with self:
            def handle_change(msg: Dict):
                handle_event(on_pick, ColorPickEventArguments(sender=self, client=self.client, color=msg['args']))
            Element('q-color').on('change', handle_change)
