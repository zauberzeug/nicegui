import traceback
from typing import Callable, Dict, Optional

from ..events import KeyboardAction, KeyboardKey, KeyboardModifiers, KeyEventArguments, handle_event
from ..routes import add_dependencies
from .custom_view import CustomView
from .element import Element

add_dependencies(__file__)


class KeyboardView(CustomView):

    def __init__(self, on_key: Callable, repeating: bool):
        super().__init__('keyboard', active_js_events=['keydown', 'keyup'], repeating=repeating)
        self.allowed_events = ['keyboardEvent']
        self.style = 'display: none'
        self.initialize(temp=False, on_keyboardEvent=on_key)


class Keyboard(Element):

    def __init__(self, *, on_key: Optional[Callable] = None, active: bool = True, repeating: bool = True):
        """
        Keyboard

        Adds global keyboard event tracking.

        :param on_key: callback to be executed when keyboard events occur.
        :param active: boolean flag indicating whether the callback should be executed or not (default: `True`)
        :param repeating: boolean flag indicating whether held keys should be sent repeatedly (default: `True`)
        """
        super().__init__(KeyboardView(on_key=self.handle_key, repeating=repeating))
        self.active = active
        self.key_handler = on_key

    def handle_key(self, msg: Dict) -> Optional[bool]:
        if not self.active:
            return False

        try:
            action = KeyboardAction(
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
            arguments = KeyEventArguments(
                sender=self,
                socket=msg.websocket,
                action=action,
                modifiers=modifiers,
                key=key
            )
            return handle_event(self.key_handler, arguments)
        except Exception:
            traceback.print_exc()
