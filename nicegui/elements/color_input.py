from typing import Any, Callable, Optional

from .button import Button as button
from .color_picker import ColorPicker as color_picker
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class ColorInput(ValueElement, DisableableElement):
    """
    Color Input

    This class represents a color input element that extends Quasar's QInput component with a color picker.

    Attributes:
        LOOPBACK (bool): Indicates whether the color input supports loopback. Default is False.

    Args:
    
        - label (str, optional): Displayed label for the color input.
        - placeholder (str, optional): Text to show if no color is selected.
        - value (str, optional): The current color value.
        - on_change (callable, optional): Callback to execute when the value changes.
        - preview (bool, optional): Change button background to selected color (default: False).

    Methods:
        - open_picker(): Open the color picker.
        - _handle_value_change(value: Any): Handle the change in value for the color input element.
        - _update_preview(): Update the preview button's background color based on the selected color.
    """

    LOOPBACK = False

    def __init__(self,
                 label: Optional[str] = None, *,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 on_change: Optional[Callable[..., Any]] = None,
                 preview: bool = False,
                 ) -> None:
        """
        Color Input

        Args:
        
            - label (str, optional): Displayed label for the color input.
            - placeholder (str, optional): Text to show if no color is selected.
            - value (str, optional): The current color value.
            - on_change (callable, optional): Callback to execute when the value changes.
            - preview (bool, optional): Change button background to selected color (default: False).
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
        """
        Open the color picker.

        This method opens the color picker dialog, allowing the user to select a color.
        If a value is already set for the color input, the picker will be initialized with that value.
        After the picker is opened, the selected color can be retrieved using the `get_color()` method.

        Usage:
            color_input = ColorInput()
            color_input.open_picker()
            selected_color = color_input.get_color()

        Returns:
            None
        """
        if self.value:
            self.picker.set_color(self.value)
        self.picker.open()

    def _handle_value_change(self, value: Any) -> None:
        """
        Handle the change in value for the color input element.

        This method is called when the value of the color input element is changed.
        It updates the preview of the color and calls the base class's _handle_value_change method.

        Parameters:
            value (Any): The new value of the color input element.

        Returns:
            None
        """
        super()._handle_value_change(value)
        self._update_preview()

    def _update_preview(self) -> None:
        """
        Update the preview button's background color based on the selected color.

        This method updates the background color of the preview button based on the selected color.
        If the preview button is not enabled, the method returns without making any changes.

        Parameters:
            None

        Returns:
            None

        Example usage:
            color_input = ColorInput()
            color_input._update_preview()
        """
        if not self.preview:
            return
        self.button.style(f'''
            background-color: {(self.value or "#fff").split(";", 1)[0]};
            text-shadow: 2px 0 #fff, -2px 0 #fff, 0 2px #fff, 0 -2px #fff, 1px 1px #fff, -1px -1px #fff, 1px -1px #fff, -1px 1px #fff;
        ''')
