from typing import Callable

from .custom_view import CustomView
from .element import Element
from ..utils import handle_exceptions, provide_arguments


class HotkeyView(CustomView):

    def __init__(self, handle_keys: Callable):
        super().__init__('hotkey', __file__, activeJSEvents=['keydown', 'keyup', 'keypress'])
        self.allowed_events = ['keyboardEvent']
        self.style = 'display: none'
        self.initialize(temp=False, on_keyboardEvent=handle_exceptions(provide_arguments(handle_keys, 'key_data', 'event_type')))


class Hotkey(Element):

    def __init__(self, handle_keys: Callable = None):
        """Hotkeys

        Adds a hotkey action to an element.

        :param keys: list of characters that the action should be associated with, e.g. ['f', 'g']
        :param on_keydown: callback to be executed when the specified keys are pressed while the parent is hovered
        """
        super().__init__(HotkeyView(handle_keys=handle_keys))
