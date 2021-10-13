from typing import Callable

from .custom_view import CustomView
from .element import Element
from ..utils import handle_exceptions, provide_arguments


class HotkeyView(CustomView):

    def __init__(self, keys: list, on_keydown: Callable):
        super().__init__('hotkey', __file__, keys=keys)
        self.on_keydown = on_keydown
        self.allowed_events = ['onKeydown', ]
        self.style = 'display: none'
        self.initialize(temp=False, onKeydown=handle_exceptions(provide_arguments(on_keydown)))


class Hotkey(Element):

    def __init__(self, keys: list, on_keydown: Callable = None):
        """Hotkeys

        Adds a hotkey action to an element.

        :param key: the character that the action should be associated with, e.g. 'f'
        :param on_keydown: callback to be executed when the specified key is pressed while the parents is active
        """
        super().__init__(HotkeyView(keys=keys, on_keydown=on_keydown))
