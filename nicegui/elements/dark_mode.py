from typing_extensions import Self

from ..defaults import DEFAULT_PROP, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .mixins.value_element import ValueElement


class DarkMode(ValueElement[bool | None], component='dark_mode.js'):
    VALUE_PROP = 'value'

    @resolve_defaults
    def __init__(self,
                 value: bool | None = DEFAULT_PROP | False, *,
                 on_change: Handler[ValueChangeEventArguments[bool | None]] | None = None,
                 ) -> None:
        """Dark mode

        You can use this element to enable, disable or toggle dark mode on the page.
        The value `None` represents auto mode, which uses the client's system preference.

        Note that this element overrides the `dark` parameter of the `ui.run` function and page decorators.

        :param value: Whether dark mode is enabled. If None, dark mode is set to auto.
        :param on_change: Callback that is invoked when the value changes.
        """
        super().__init__(value=value, on_value_change=on_change)

    def enable(self) -> Self:
        """Enable dark mode."""
        self.value = True
        return self

    def disable(self) -> Self:
        """Disable dark mode."""
        self.value = False
        return self

    def toggle(self) -> Self:
        """Toggle dark mode.

        This method will raise a ValueError if dark mode is set to auto.
        """
        if self.value is None:
            raise ValueError('Cannot toggle dark mode when it is set to auto.')
        self.value = not self.value
        return self

    def auto(self) -> Self:
        """Set dark mode to auto.

        This will use the client's system preference.
        """
        self.value = None
        return self
