from typing import Optional

from ..events import Handler, ValueChangeEventArguments
from .mixins.value_element import ValueElement


class Fullscreen(ValueElement, component='fullscreen.js'):
    LOOPBACK = None

    def __init__(self, *,
                 require_escape_hold: bool = False,
                 on_value_change: Optional[Handler[ValueChangeEventArguments]] = None) -> None:
        """Fullscreen control element

        This element is based on Quasar's `AppFullscreen <https://quasar.dev/quasar-plugins/app-fullscreen>`_ plugin
        and provides a way to enter, exit and toggle the fullscreen mode.

        Important notes:

        * Due to security reasons, the fullscreen mode can only be entered from a previous user interaction such as a button click.
        * The long-press escape requirement only works in some browsers like Google Chrome or Microsoft Edge.

        *Added in version 2.11.0*

        :param require_escape_hold: whether the user needs to long-press the escape key to exit fullscreen mode
        :param on_value_change: callback which is invoked when the fullscreen state changes
        """
        super().__init__(value=False, on_value_change=on_value_change)
        self._props['requireEscapeHold'] = require_escape_hold

    @property
    def require_escape_hold(self) -> bool:
        """Whether the user needs to long-press of the escape key to exit fullscreen mode.

        This feature is only supported in some browsers like Google Chrome or Microsoft Edge.
        In unsupported browsers, this setting has no effect.
        """
        return self._props['requireEscapeHold']

    @require_escape_hold.setter
    def require_escape_hold(self, value: bool) -> None:
        self._props['requireEscapeHold'] = value
        self.update()

    def enter(self) -> None:
        """Enter fullscreen mode."""
        self.value = True

    def exit(self) -> None:
        """Exit fullscreen mode."""
        self.value = False

    def toggle(self) -> None:
        """Toggle fullscreen mode."""
        self.value = not self.value

    def _handle_value_change(self, value: bool) -> None:
        super()._handle_value_change(value)
        self.run_method('enter' if value else 'exit')
