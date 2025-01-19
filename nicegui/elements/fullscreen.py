from typing import Callable, Optional

from ..element import Element
from ..events import GenericEventArguments, ValueChangeEventArguments


class Fullscreen(Element, component='fullscreen.js'):

    def __init__(self, *,
                 require_escape_hold: bool = False,
                 on_state_change: Optional[Callable[[ValueChangeEventArguments], None]] = None) -> None:
        """Fullscreen control element

        This element is based on Quasar's `AppFullscreen <https://quasar.dev/quasar-plugins/app-fullscreen>`_ plugin
        and provides a way to enter, exit and toggle the fullscreen mode.

        Important notes:

        * Due to security reasons, the fullscreen mode can only be entered from a previous user interaction such as a button click.
        * The long-press escape requirement only works in some browsers like Google Chrome or Microsoft Edge.

        *Added in version 2.10.0*

        :param require_escape_hold: whether the user needs to long-press the escape key to exit fullscreen mode
        :param on_state_change: callback which is invoked when the fullscreen state changes
        """
        super().__init__()
        self._is_fullscreen = False
        self._require_escape_hold = require_escape_hold
        self.on('fullscreen_change', self._handle_fullscreen_change)
        self._state_change_handlers = [on_state_change] if on_state_change else []

    def _handle_fullscreen_change(self, event: GenericEventArguments) -> None:
        self._is_fullscreen = event.args
        for handler in self._state_change_handlers:
            handler(ValueChangeEventArguments(sender=self, client=self.client, value=self._is_fullscreen))

    @property
    def require_escape_hold(self) -> bool:
        """Whether the user needs to long-press of the escape key to exit fullscreen mode.

        This feature is only supported in some browsers like Google Chrome or Microsoft Edge.
        In unsupported browsers, this setting has no effect.
        """
        return self._require_escape_hold

    @require_escape_hold.setter
    def require_escape_hold(self, value: bool) -> None:
        self._require_escape_hold = value

    def on_state_change(self, handler: Callable[[ValueChangeEventArguments], None]) -> None:
        """Register a handler for fullscreen state changes.

        :param handler: handler which is invoked when the fullscreen state changes
        """
        self._state_change_handlers.append(handler)

    @property
    def state(self) -> bool:
        """The current fullscreen state.

        The state can only be modified programmatically if the user interacted with a control.
        """
        return self._is_fullscreen

    @state.setter
    def state(self, value: bool) -> None:
        if value:
            self.enter()
        else:
            self.exit()

    def enter(self) -> None:
        """Enter fullscreen mode."""
        self.run_method('enter', self._require_escape_hold)

    def exit(self) -> None:
        """Exit fullscreen mode."""
        self.run_method('exit')

    def toggle(self) -> None:
        """Toggle fullscreen mode.

        The state can only be modified programmatically if the user interacted with a control.
        """
        self.run_method('toggle', self._require_escape_hold)
