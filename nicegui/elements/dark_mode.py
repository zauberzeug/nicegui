from typing import Optional

from .. import core, helpers
from ..events import Handler, ValueChangeEventArguments
from .mixins.value_element import ValueElement


class DarkMode(ValueElement, component='dark_mode.js'):
    VALUE_PROP = 'value'

    def __init__(self, value: Optional[bool] = False, *, on_change: Optional[Handler[ValueChangeEventArguments]] = None) -> None:
        """Dark mode

        You can use this element to enable, disable or toggle dark mode on the page.
        The value `None` represents auto mode, which uses the client's system preference.

        Note that this element overrides the `dark` parameter of the `ui.run` function and page decorators.

        :param value: Whether dark mode is enabled. If None, dark mode is set to auto.
        :param on_change: Callback that is invoked when the value changes.
        """
        super().__init__(value=value, on_value_change=on_change)

        # HACK: this is a temporary warning to inform users about issue #3753
        if core.app.is_started:
            self._check_for_issue_3753()
        else:
            core.app.on_startup(self._check_for_issue_3753)

    def _check_for_issue_3753(self) -> None:
        if self.client.page.resolve_dark() is None and core.app.config.tailwind:
            helpers.warn_once(
                '`ui.dark_mode` is not supported on pages with `dark=None` while running with `tailwind=True` (the default). '
                'See https://github.com/zauberzeug/nicegui/issues/3753 for more information.'
            )

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
