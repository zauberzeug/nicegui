import traceback
from typing import Awaitable, Callable, Dict, Optional, Union

from ..events import KeyEventArguments, KeyboardAction, KeyboardKey, KeyboardModifiers, handle_event
from .custom_view import CustomView
from .element import Element

class KeyboardView(CustomView):

    def __init__(self, on_key: Callable, repeating: bool):
        super().__init__('keyboard', __file__, active_js_events=['keydown', 'keyup', 'keypress'], repeating=repeating)
        self.allowed_events = ['keyboardEvent']
        self.style = 'display: none'
        self.initialize(temp=False, on_keyboardEvent=on_key)


class Keyboard(Element):

    def __init__(self,
                 *,
                 on_key: Optional[Union[Callable, Awaitable]] = None,
                 active: bool = True,
                 repeating: bool = True,
                 ):
        """
        Keyboard

        Adds global keyboard event tracking.

        :param handle_keys: callback to be executed when keyboard events occur.
        :param active: boolean flag indicating whether the callback should be executed or not (default: True)
        :param repeating: boolean flag indicating whether held keys should be sent repeatedly (default: True)
        """
        super().__init__(KeyboardView(on_key=self.handle_key, repeating=repeating))
        self.active = active
        self.key_handler = on_key

    def handle_key(self, msg: Dict):
        if not self.active:
            return

        try:
            action = KeyboardAction(
                keypress=msg.key_data.action == 'keypress',
                keydown=msg.key_data.action == 'keydown',
                keyup=msg.key_data.action == 'keyup',
                repeat=msg.key_data.repeat,
            )
            modifiers = KeyboardModifiers(
                alt=msg.key_data.altKey,
                ctrl=msg.key_data.ctrlKey,
                meta=msg.key_data.metaKey,
                shift=msg.key_data.shiftKey,
            )
            key = KeyboardKey(
                name=msg.key_data.key,
                code=msg.key_data.code,
                location=msg.key_data.location,
            )
            arguments = KeyEventArguments(sender=self, action=action, modifiers=modifiers, key=key)
            handle_event(self.key_handler, arguments, update=self.parent_view)
        except Exception:
            traceback.print_exc()
