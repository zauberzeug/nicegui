from typing import Callable

from .custom_view import CustomView
from .element import Element
from ..utils import handle_exceptions, provide_arguments


class KeyboardView(CustomView):

    def __init__(self, handle_keys: Callable, active: bool = True):
        super().__init__('keyboard', __file__, activeJSEvents=['keydown', 'keyup', 'keypress'])
        self.allowed_events = ['keyboardEvent']
        self.style = 'display: none'
        self.active = active

        def execute_when_active(*args):
            if self.active:
                handle_exceptions(provide_arguments(handle_keys, 'key_data', 'event_type'))(*args)

        self.initialize(temp=False, on_keyboardEvent=execute_when_active)


class Keyboard(Element):

    def __init__(self, handle_keys: Callable = None, active: bool = True):
        """
        Keyboard

        Adds global keyboard event tracking.

        :param handle_keys: callback to be executed when keyboard events occur.
        :param active: boolean flag indicating whether the callback should be executed or not
        """
        super().__init__(KeyboardView(handle_keys=handle_keys, active=active))
