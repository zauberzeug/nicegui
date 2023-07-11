from dataclasses import dataclass
from inspect import Parameter, signature
from typing import TYPE_CHECKING, Any, Awaitable, BinaryIO, Callable, Dict, List, Optional

from . import background_tasks, globals
from .helpers import KWONLY_SLOTS

if TYPE_CHECKING:
    from .client import Client
    from .element import Element


@dataclass(**KWONLY_SLOTS)
class EventArguments:
    sender: 'Element'
    client: 'Client'


@dataclass(**KWONLY_SLOTS)
class GenericEventArguments(EventArguments):
    args: Dict[str, Any]

    def __getitem__(self, key: str) -> Any:
        if key == 'args':
            globals.log.warning('msg["args"] is deprecated, use e.args instead '
                                '(see https://github.com/zauberzeug/nicegui/pull/1095)')
            return self.args
        raise KeyError(key)


@dataclass(**KWONLY_SLOTS)
class ClickEventArguments(EventArguments):
    pass


@dataclass(**KWONLY_SLOTS)
class SceneClickHit:
    object_id: str
    object_name: str
    x: float
    y: float
    z: float


@dataclass(**KWONLY_SLOTS)
class SceneClickEventArguments(ClickEventArguments):
    click_type: str
    button: int
    alt: bool
    ctrl: bool
    meta: bool
    shift: bool
    hits: List[SceneClickHit]


@dataclass(**KWONLY_SLOTS)
class ColorPickEventArguments(EventArguments):
    color: str


@dataclass(**KWONLY_SLOTS)
class MouseEventArguments(EventArguments):
    type: str
    image_x: float
    image_y: float
    button: int
    buttons: int
    alt: bool
    ctrl: bool
    meta: bool
    shift: bool


@dataclass(**KWONLY_SLOTS)
class JoystickEventArguments(EventArguments):
    action: str
    x: Optional[float] = None
    y: Optional[float] = None


@dataclass(**KWONLY_SLOTS)
class UploadEventArguments(EventArguments):
    content: BinaryIO
    name: str
    type: str


@dataclass(**KWONLY_SLOTS)
class ValueChangeEventArguments(EventArguments):
    value: Any


@dataclass(**KWONLY_SLOTS)
class TableSelectionEventArguments(EventArguments):
    selection: List[Any]


@dataclass(**KWONLY_SLOTS)
class KeyboardAction:
    keydown: bool
    keyup: bool
    repeat: bool


@dataclass(**KWONLY_SLOTS)
class KeyboardModifiers:
    alt: bool
    ctrl: bool
    meta: bool
    shift: bool


@dataclass(**KWONLY_SLOTS)
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


@dataclass(**KWONLY_SLOTS)
class KeyEventArguments(EventArguments):
    action: KeyboardAction
    key: KeyboardKey
    modifiers: KeyboardModifiers


@dataclass(**KWONLY_SLOTS)
class ScrollEventArguments(EventArguments):
    vertical_position: float
    vertical_percentage: float
    vertical_size: float
    vertical_container_size: float
    horizontal_position: float
    horizontal_percentage: float
    horizontal_size: float
    horizontal_container_size: float


def handle_event(handler: Optional[Callable[..., Any]], arguments: EventArguments) -> None:
    if handler is None:
        return
    try:
        expects_arguments = any(p.default is Parameter.empty and
                                p.kind is not Parameter.VAR_POSITIONAL and
                                p.kind is not Parameter.VAR_KEYWORD
                                for p in signature(handler).parameters.values())
        if arguments.sender.is_ignoring_events:
            return
        with arguments.sender.parent_slot:
            result = handler(arguments) if expects_arguments else handler()
        if isinstance(result, Awaitable):
            async def wait_for_result():
                with arguments.sender.parent_slot:
                    await result
            if globals.loop and globals.loop.is_running():
                background_tasks.create(wait_for_result(), name=str(handler))
            else:
                globals.app.on_startup(wait_for_result())
    except Exception as e:
        globals.handle_exception(e)
