from typing import Any, Callable

from ..element import Element
from ..events import ColorPickEventArguments, GenericEventArguments, handle_event
from .menu import Menu


class ColorPicker(Menu):
    """
    A color picker element based on Quasar's QMenu and QColor components.

    Usage:
    ------
    color_picker = ColorPicker(on_pick=callback_function, value=False)
    color_picker.set_color("#FF0000")

    Parameters:
    -----------
    on_pick : Callable[..., Any]
        A callback function to execute when a color is picked. The function should accept
        a single argument, which is an instance of ColorPickEventArguments.
    value : bool, optional
        Whether the menu is already opened. Default is False.

    Methods:
    --------
    set_color(color: str) -> None:
        Set the color of the picker.

    Attributes:
    -----------
    q_color : Element
        The underlying q-color component.

    Examples:
    ---------
    # Create a color picker with a callback function
    def on_color_pick(event: ColorPickEventArguments):
        print(f"Color picked: {event.color}")

    color_picker = ColorPicker(on_pick=on_color_pick)

    # Set the initial color
    color_picker.set_color("#FF0000")
    """

    def __init__(self, *, on_pick: Callable[..., Any], value: bool = False) -> None:
        """
        Initialize the ColorPicker.

        Parameters:
        -----------
        on_pick : Callable[..., Any]
            A callback function to execute when a color is picked. The function should accept
            a single argument, which is an instance of ColorPickEventArguments.
        value : bool, optional
            Whether the menu is already opened. Default is False.
        """
        super().__init__(value=value)
        with self:
            def handle_change(e: GenericEventArguments):
                handle_event(on_pick, ColorPickEventArguments(sender=self, client=self.client, color=e.args))
            self.q_color = Element('q-color').on('change', handle_change)

    def set_color(self, color: str) -> None:
        """
        Set the color of the picker.

        Parameters:
        -----------
        color : str
            The color to set.
        """
        self.q_color.props(f'model-value="{color}"')
