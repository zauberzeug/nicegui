from typing import Any, Callable, Optional

from .mixins.value_element import ValueElement


class DarkMode(ValueElement, component='dark_mode.js'):
    """
    A class representing a dark mode element.

    This element can be used to enable, disable, or toggle dark mode on a page.
    The value `None` represents auto mode, which uses the client's system preference.

    Note that this element overrides the `dark` parameter of the `ui.run` function and page decorators.

    Attributes:
        VALUE_PROP (str): The property name for the value of the dark mode element.

    Args:
        value (bool, optional): Whether dark mode is enabled. If None, dark mode is set to auto. Defaults to False.
        on_change (callable, optional): Callback that is invoked when the value changes.

    Methods:
        enable(): Enable dark mode.
        disable(): Disable dark mode.
        toggle(): Toggle dark mode.
        auto(): Set dark mode to auto.

    Example:
        dark_mode = DarkMode(value=True)
        dark_mode.disable()
        dark_mode.toggle()
    """

    VALUE_PROP = 'value'

    def __init__(self, value: Optional[bool] = False, *, on_change: Optional[Callable[..., Any]] = None) -> None:
        """
        Initialize a DarkMode instance.

        Args:
            value (bool, optional): Whether dark mode is enabled. If None, dark mode is set to auto. Defaults to False.
            on_change (callable, optional): Callback that is invoked when the value changes.
        """
        super().__init__(value=value, on_value_change=on_change)

    def enable(self) -> None:
        """Enable dark mode."""
        self.value = True

    def disable(self) -> None:
        """Disable dark mode."""
        self.value = False

    def toggle(self) -> None:
        """
        Toggle dark mode.

        Raises:
            ValueError: If dark mode is set to auto.
        """
        if self.value is None:
            raise ValueError('Cannot toggle dark mode when it is set to auto.')
        self.value = not self.value

    def auto(self) -> None:
        """Set dark mode to auto."""
        self.value = None
