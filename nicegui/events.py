import traceback
from dataclasses import dataclass
from inspect import signature
from typing import TYPE_CHECKING, Any, BinaryIO, Callable, List, Optional, Union

from . import background_tasks, globals
from .async_updater import AsyncUpdater
from .helpers import is_coroutine

if TYPE_CHECKING:
    from .client import Client
    from .element import Element


@dataclass
class EventArguments:
    sender: 'Element'
    client: 'Client'


@dataclass
class ClickEventArguments(EventArguments):
    pass


@dataclass
class SceneClickHit:
    object_id: str
    object_name: str
    x: float
    y: float
    z: float


@dataclass
class SceneClickEventArguments(ClickEventArguments):
    click_type: str
    button: int
    alt: bool
    ctrl: bool
    meta: bool
    shift: bool
    hits: List[SceneClickHit]


@dataclass
class ColorPickEventArguments(EventArguments):
    color: str


@dataclass
class MouseEventArguments(EventArguments):
    type: str
    image_x: float
    image_y: float


@dataclass
class JoystickEventArguments(EventArguments):
    action: str
    x: Optional[float] = None
    y: Optional[float] = None


@dataclass
class UploadEventArguments(EventArguments):
    content: BinaryIO
    name: str
    type: str


@dataclass
class ValueChangeEventArguments(EventArguments):
    value: Any


@dataclass
class KeyboardAction:
    keydown: bool
    keyup: bool
    repeat: bool


@dataclass
class KeyboardModifiers:
    alt: bool
    ctrl: bool
    meta: bool
    shift: bool


@dataclass
class KeyboardKey:
    name: str
    code: str
    location: int

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.name == other or self.code == other
        elif isinstance(other, KeyboardKey):
            return self == other
        else:
            return False

    def __repr__(self):
        return str(self.name)

    @property
    def is_cursorkey(self):
        return self.code.startswith('Arrow')

    @property
    def number(self) -> Optional[int]:
        """Integer value of a number key."""
        return int(self.code.removeprefix('Digit')) if self.code.startswith('Digit') else None

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


@dataclass
class KeyEventArguments(EventArguments):
    action: KeyboardAction
    key: KeyboardKey
    modifiers: KeyboardModifiers


def handle_event(handler: Optional[Callable],
                 arguments: Union[EventArguments, dict], *,
                 sender: Optional['Element'] = None) -> None:
    try:
        if handler is None:
            return
        no_arguments = not signature(handler).parameters
        sender = arguments.sender if isinstance(arguments, EventArguments) else sender
        assert sender.parent_slot is not None
        with sender.parent_slot:
            result = handler() if no_arguments else handler(arguments)
        if is_coroutine(handler):
            async def wait_for_result():
                with sender.parent_slot:
                    await AsyncUpdater(result)
            if globals.loop and globals.loop.is_running():
                background_tasks.create(wait_for_result(), name=str(handler))
            else:
                globals.app.on_startup(wait_for_result())
    except Exception:
        traceback.print_exc()
