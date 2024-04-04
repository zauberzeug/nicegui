from typing import Any, Callable, Optional

from .button import Button
from .mixins.value_element import ValueElement


class DropdownButton(Button, ValueElement):

    def __init__(self,
                 text: str = '', *,
                 value: bool = False,
                 on_value_change: Optional[Callable[..., Any]] = None,
                 on_click: Optional[Callable[..., Any]] = None,
                 color: Optional[str] = 'primary',
                 icon: Optional[str] = None,
                 auto_close: Optional[bool] = False,
                 split: Optional[bool] = False,
                 ) -> None:
        """Dropdown Button

        This element is based on Quasar's `QBtnDropDown <https://quasar.dev/vue-components/button-dropdown>`_ component.

        The ``color`` parameter accepts a Quasar color, a Tailwind color, or a CSS color.
        If a Quasar color is used, the button will be styled according to the Quasar theme including the color of the text.
        Note that there are colors like "red" being both a Quasar color and a CSS color.
        In such cases the Quasar color will be used.

        :param text: the label of the button
        :param value: if the dropdown is open or not (default: `False`)
        :param on_value_change: callback which is invoked when the dropdown is opened or closed
        :param on_click: callback which is invoked when button is pressed
        :param color: the color of the button (either a Quasar, Tailwind, or CSS color or `None`, default: 'primary')
        :param icon: the name of an icon to be displayed on the button (default: `None`)
        :param auto_close: whether the dropdown should close automatically when an item is clicked (default: `False`)
        :param split: whether to split the dropdown icon into a separate button (default: `False`)
        """
        super().__init__(text=text, on_click=on_click, color=color, icon=icon,
                         value=value, on_value_change=on_value_change)
        self.tag = 'q-btn-dropdown'

        if auto_close:
            self._props['auto-close'] = True

        if split:
            self._props['split'] = True

    def open(self) -> None:
        """Open the dropdown."""
        self.value = True

    def close(self) -> None:
        """Close the dropdown."""
        self.value = False

    def toggle(self) -> None:
        """Toggle the dropdown."""
        self.value = not self.value
