from typing import Any, Callable

from ..element import Element
from ..events import ColorPickEventArguments, GenericEventArguments, handle_event
from .menu import Menu


class ColorPicker(Menu):

    def __init__(self, *, on_pick: Callable[..., Any], value: bool = False) -> None:
        """Color Picker

        :param on_pick: callback to execute when a color is picked
        :param value: whether the menu is already opened (default: `False`)
        """
        super().__init__(value=value)
        with self:
            def handle_change(e: GenericEventArguments):
                handle_event(on_pick, ColorPickEventArguments(sender=self, client=self.client, color=e.args))
            self.q_color = Element('q-color').on('change', handle_change)

    def set_color(self, color: str) -> None:
        """Set the color of the picker

        :param color: the color to set
        """
        self.q_color.props(f'model-value="{color}"')
