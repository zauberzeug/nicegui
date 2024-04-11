from typing import Any, Callable, List, Literal, Optional

from typing_extensions import Self

from ..binding import BindableProperty
from ..element import Element
from ..events import (
    GenericEventArguments,
    KeyboardAction,
    KeyboardKey,
    KeyboardModifiers,
    KeyEventArguments,
    handle_event,
)


class Keyboard(Element, component='keyboard.js'):
    active = BindableProperty()

    def __init__(self,
                 on_key: Optional[Callable[..., Any]] = None, *,
                 active: bool = True,
                 repeating: bool = True,
                 ignore: List[Literal['input', 'select', 'button', 'textarea']] = [
                     'input', 'select', 'button', 'textarea'],
                 ) -> None:
        """Keyboard

        Adds global keyboard event tracking.

        :param on_key: callback to be executed when keyboard events occur.
        :param active: boolean flag indicating whether the callback should be executed or not (default: `True`)
        :param repeating: boolean flag indicating whether held keys should be sent repeatedly (default: `True`)
        :param ignore: ignore keys when one of these element types is focussed (default: `['input', 'select', 'button', 'textarea']`)
        """
        super().__init__()
        self._key_handlers = [on_key] if on_key else []
        self.active = active
        self._props['events'] = ['keydown', 'keyup']
        self._props['repeating'] = repeating
        self._props['ignore'] = ignore
        self.on('key', self._handle_key)

    def _handle_key(self, e: GenericEventArguments) -> None:
        if not self.active:
            return

        action = KeyboardAction(
            keydown=e.args['action'] == 'keydown',
            keyup=e.args['action'] == 'keyup',
            repeat=e.args['repeat'],
        )
        modifiers = KeyboardModifiers(
            alt=e.args['altKey'],
            ctrl=e.args['ctrlKey'],
            meta=e.args['metaKey'],
            shift=e.args['shiftKey'],
        )
        key = KeyboardKey(
            name=e.args['key'],
            code=e.args['code'],
            location=e.args['location'],
        )
        arguments = KeyEventArguments(
            sender=self,
            client=self.client,
            action=action,
            modifiers=modifiers,
            key=key,
        )
        for handler in self._key_handlers:
            handle_event(handler, arguments)

    def on_key(self, handler: Callable[..., Any]) -> Self:
        """Add a callback to be invoked when keyboard events occur."""
        self._key_handlers.append(handler)
        return self
