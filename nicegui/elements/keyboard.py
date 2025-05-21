from typing import List, Literal, Optional

from typing_extensions import Self

from ..binding import BindableProperty
from ..element import Element
from ..events import (
    GenericEventArguments,
    Handler,
    KeyboardAction,
    KeyboardKey,
    KeyboardModifiers,
    KeyEventArguments,
    handle_event,
)


class Keyboard(Element, component='keyboard.js'):
    active = BindableProperty()

    def __init__(self,
                 on_key: Optional[Handler[KeyEventArguments]] = None, *,
                 active: bool = True,
                 repeating: bool = True,
                 ignore: List[Literal['input', 'select', 'button', 'textarea']] =
                     ['input', 'select', 'button', 'textarea'],  # noqa: B006
                 ) -> None:
        """Keyboard

        Adds global keyboard event tracking.

        The ``on_key`` callback receives a ``KeyEventArguments`` object with the following attributes:

        - ``sender``: the ``Keyboard`` element
        - ``client``: the client object
        - ``action``: a ``KeyboardAction`` object with the following attributes:
            - ``keydown``: whether the key was pressed
            - ``keyup``: whether the key was released
            - ``repeat``: whether the key event was a repeat
        - ``key``: a ``KeyboardKey`` object with the following attributes:
            - ``name``: the name of the key (e.g. "a", "Enter", "ArrowLeft"; see `here <https://developer.mozilla.org/en-US/docs/Web/API/UI_Events/Keyboard_event_key_values>`_ for a list of possible values)
            - ``code``: the code of the key (e.g. "KeyA", "Enter", "ArrowLeft")
            - ``location``: the location of the key (0 for standard keys, 1 for left keys, 2 for right keys, 3 for numpad keys)
        - ``modifiers``: a ``KeyboardModifiers`` object with the following attributes:
            - ``alt``: whether the alt key was pressed
            - ``ctrl``: whether the ctrl key was pressed
            - ``meta``: whether the meta key was pressed
            - ``shift``: whether the shift key was pressed

        For convenience, the ``KeyboardKey`` object also has the following properties:
            - ``is_cursorkey``: whether the key is a cursor (arrow) key
            - ``number``: the integer value of a number key (0-9, ``None`` for other keys)
            - ``backspace``, ``tab``, ``enter``, ``shift``, ``control``, ``alt``, ``pause``, ``caps_lock``, ``escape``, ``space``,
              ``page_up``, ``page_down``, ``end``, ``home``, ``arrow_left``, ``arrow_up``, ``arrow_right``, ``arrow_down``,
              ``print_screen``, ``insert``, ``delete``, ``meta``,
              ``f1``, ``f2``, ``f3``, ``f4``, ``f5``, ``f6``, ``f7``, ``f8``, ``f9``, ``f10``, ``f11``, ``f12``: whether the key is the respective key

        :param on_key: callback to be executed when keyboard events occur.
        :param active: boolean flag indicating whether the callback should be executed or not (default: ``True``)
        :param repeating: boolean flag indicating whether held keys should be sent repeatedly (default: ``True``)
        :param ignore: ignore keys when one of these element types is focussed (default: ``['input', 'select', 'button', 'textarea']``)
        """
        super().__init__()
        self._key_handlers = [on_key] if on_key else []
        self.active = active
        self._props['events'] = ['keydown', 'keyup']
        self._props['repeating'] = repeating
        self._props['ignore'] = ignore[:]
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

    def on_key(self, handler: Handler[KeyEventArguments]) -> Self:
        """Add a callback to be invoked when keyboard events occur."""
        self._key_handlers.append(handler)
        return self
