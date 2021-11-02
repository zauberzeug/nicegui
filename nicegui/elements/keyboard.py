from pydantic import BaseModel
from typing import Callable, Optional

from ..binding import bind_to
from ..utils import handle_exceptions, provide_arguments
from .custom_view import CustomView
from .element import Element

class KeyboardView(CustomView):

    def __init__(self, handle_keys: Callable, active: bool = True):
        super().__init__('keyboard', __file__, activeJSEvents=['keydown', 'keyup', 'keypress'])
        self.allowed_events = ['keyboardEvent']
        self.style = 'display: none'
        self.active = active

        def execute_when_active(*args):
            if not self.active:
                return

            event_args = args[1]
            event_args.action = KeyboardAction(
                keypress=event_args.key_data['action'] == 'keypress',
                keydown=event_args.key_data['action'] == 'keydown',
                keyup=event_args.key_data['action'] == 'keyup',
                repeat=event_args.key_data['repeat'],
            )
            event_args.modifiers = KeyboardModifiers(
                alt=event_args.key_data['altKey'],
                ctrl=event_args.key_data['ctrlKey'],
                meta=event_args.key_data['metaKey'],
                shift=event_args.key_data['shiftKey'],
            )
            event_args.key = KeyboardKey(
                name=event_args.key_data['key'],
                code=event_args.key_data['code'],
                location=event_args.key_data['location'],
            )

            handle_exceptions(provide_arguments(handle_keys, 'key_data', 'action', 'modifiers', 'key'))(*args)

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
        self.active = active
        bind_to(self, 'active', self.view, 'active', lambda x: x)

class KeyboardAction(BaseModel):
    keypress: bool
    keydown: bool
    keyup: bool
    repeat: bool

class KeyboardModifiers(BaseModel):
    alt: bool
    ctrl: bool
    meta: bool
    shift: bool

class KeyboardKey(BaseModel):
    name: str
    code: str
    location: int

    def __eq__(self, other: str) -> bool:
        return self.name == other or self.code == other

    def __repr__(self):
        return str(self.name)

    @property
    def is_cursorkey(self):
        return self.code.startswith('Arrow')

    @property
    def number(self) -> Optional[int]:
        """Integer value of a number key."""
        return int(self.name) if self.code.startswith('Digit') else None

    @property
    def backspace(self) -> bool:
        return self.name == 'Backspace'

    @property
    def tab(self) -> bool:
        return self.name == 'Tab'

    @property
    def enter(self) -> bool:
        return self.name == 'enter'

    @property
    def shift(self) -> bool:
        return self.name == 'Shift'

    @property
    def control(self) -> bool:
        return self.name == 'Control'

    @property
    def alt(self) -> bool:
        return self.name == 'Alt'

    @property
    def pause(self) -> bool:
        return self.name == 'Pause'

    @property
    def caps_lock(self) -> bool:
        return self.name == 'CapsLock'

    @property
    def escape(self) -> bool:
        return self.name == 'Escape'

    @property
    def space(self) -> bool:
        return self.name == 'Space'

    @property
    def page_up(self) -> bool:
        return self.name == 'PageUp'

    @property
    def page_down(self) -> bool:
        return self.name == 'PageDown'

    @property
    def end(self) -> bool:
        return self.name == 'End'

    @property
    def home(self) -> bool:
        return self.name == 'Home'

    @property
    def arrow_left(self) -> bool:
        return self.name == 'ArrowLeft'

    @property
    def arrow_up(self) -> bool:
        return self.name == 'ArrowUp'

    @property
    def arrow_right(self) -> bool:
        return self.name == 'ArrowRight'

    @property
    def arrow_down(self) -> bool:
        return self.name == 'ArrowDown'

    @property
    def print_screen(self) -> bool:
        return self.name == 'PrintScreen'

    @property
    def insert(self) -> bool:
        return self.name == 'Insert'

    @property
    def delete(self) -> bool:
        return self.name == 'Delete'

    @property
    def meta(self) -> bool:
        return self.name == 'Meta'

    @property
    def f1(self) -> bool:
        return self.name == 'F1'

    @property
    def f2(self) -> bool:
        return self.name == 'F2'

    @property
    def f3(self) -> bool:
        return self.name == 'F3'

    @property
    def f4(self) -> bool:
        return self.name == 'F4'

    @property
    def f5(self) -> bool:
        return self.name == 'F5'

    @property
    def f6(self) -> bool:
        return self.name == 'F6'

    @property
    def f7(self) -> bool:
        return self.name == 'F7'

    @property
    def f8(self) -> bool:
        return self.name == 'F8'

    @property
    def f9(self) -> bool:
        return self.name == 'F9'

    @property
    def f10(self) -> bool:
        return self.name == 'F10'

    @property
    def f11(self) -> bool:
        return self.name == 'F11'

    @property
    def f12(self) -> bool:
        return self.name == 'F12'
