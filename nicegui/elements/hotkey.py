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
        """
        Hotkeys

        Adds global keyboard event tracking.

        :param handle_keys: callback to be executed when keyboard events occur.
        """

        super().__init__(HotkeyView(handle_keys=handle_keys))
