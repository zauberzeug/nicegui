from typing import Optional

from .mixins.value_element import ValueElement


class DarkMode(ValueElement, component='dark_mode.js'):
    VALUE_PROP = 'value'

    def __init__(self, value: Optional[bool] = False) -> None:
        """Dark mode

        You can use this element to enable, disable or toggle dark mode on the page.
        The value `None` represents auto mode, which uses the client's system preference.

        Note that this element overrides the `dark` parameter of the `ui.run` function and page decorators.

        :param value: Whether dark mode is enabled. If None, dark mode is set to auto.
        """
        super().__init__(value=value, on_value_change=None)

    def enable(self) -> None:
        """Enable dark mode."""
        self.value = True

    def disable(self) -> None:
        """Disable dark mode."""
        self.value = False

    def toggle(self) -> None:
        """Toggle dark mode.

        This method will raise a ValueError if dark mode is set to auto.
        """
        if self.value is None:
            raise ValueError('Cannot toggle dark mode when it is set to auto.')
        self.value = not self.value

    def auto(self) -> None:
        """Set dark mode to auto.

        This will use the client's system preference.
        """
        self.value = None
