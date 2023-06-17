from typing import Any, Callable, Dict, List

from typing_extensions import Literal

from ..binding import BindableProperty
from ..dependencies import register_component
from ..element import Element
from ..events import KeyboardAction, KeyboardKey, KeyboardModifiers, KeyEventArguments, handle_event

register_component('keyboard', __file__, 'keyboard.js')


class Keyboard(Element):
    active = BindableProperty()

    def __init__(self,
                 on_key: Callable[..., Any], *,
                 active: bool = True,
                 repeating: bool = True,
                 ignore: List[Literal['input', 'select', 'button', 'textarea']] = ['input', 'select', 'button', 'textarea'],
                 ) -> None:
        """Keyboard

        Adds global keyboard event tracking.

        :param on_key: callback to be executed when keyboard events occur.
        :param active: boolean flag indicating whether the callback should be executed or not (default: `True`)
        :param repeating: boolean flag indicating whether held keys should be sent repeatedly (default: `True`)
        :param ignore: ignore keys when one of these element types is focussed (default: `['input', 'select', 'button', 'textarea']`)
        """
        super().__init__('keyboard')
        self.key_handler = on_key
        self.active = active
        self._props['events'] = ['keydown', 'keyup']
        self._props['repeating'] = repeating
        self._props['ignore'] = ignore
        self.on('key', self.handle_key)

    def handle_key(self, msg: Dict) -> None:
        if not self.active:
            return

        action = KeyboardAction(
            keydown=msg['args']['action'] == 'keydown',
            keyup=msg['args']['action'] == 'keyup',
            repeat=msg['args']['repeat'],
        )
        modifiers = KeyboardModifiers(
            alt=msg['args']['altKey'],
            ctrl=msg['args']['ctrlKey'],
            meta=msg['args']['metaKey'],
            shift=msg['args']['shiftKey'],
        )
        key = KeyboardKey(
            name=msg['args']['key'],
            code=msg['args']['code'],
            location=msg['args']['location'],
        )
        arguments = KeyEventArguments(
            sender=self,
            client=self.client,
            action=action,
            modifiers=modifiers,
            key=key,
        )
        return handle_event(self.key_handler, arguments)
