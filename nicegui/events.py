from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Iterator
from contextlib import nullcontext
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal, TypeAlias, TypeVar, cast

from . import background_tasks, core, helpers
from .awaitable_response import AwaitableResponse
from .dataclasses import KWONLY_SLOTS
from .slot import Slot

if TYPE_CHECKING:
    from .client import Client
    from .element import Element
    from .elements.slide_item import SlideSide
    from .elements.upload_files import FileUpload
    from .observables import ObservableCollection


@dataclass(**KWONLY_SLOTS)
class EventArguments:
    pass


@dataclass(**KWONLY_SLOTS)
class ObservableChangeEventArguments(EventArguments):
    sender: ObservableCollection


@dataclass(**KWONLY_SLOTS)
class UiEventArguments(EventArguments):
    sender: Element
    client: Client


@dataclass(**KWONLY_SLOTS)
class GenericEventArguments(UiEventArguments):
    args: Any


@dataclass(**KWONLY_SLOTS)
class ClickEventArguments(UiEventArguments):
    pass


@dataclass(**KWONLY_SLOTS)
class SlideEventArguments(UiEventArguments):
    side: SlideSide


@dataclass(**KWONLY_SLOTS)
class EChartComponentClickEventArguments(UiEventArguments):
    component_type: str
    name: str | None


@dataclass(**KWONLY_SLOTS)
class EChartPointClickEventArguments(UiEventArguments):
    component_type: str
    name: str
    series_type: str
    series_index: int
    series_name: str
    data_index: int
    data: float | int | str
    data_type: str | None
    value: float | int | list


@dataclass(**KWONLY_SLOTS)
class MermaidNodeClickEventArguments(UiEventArguments):
    node_id: str


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
    hits: list[SceneClickHit]


@dataclass(**KWONLY_SLOTS)
class SceneDragEventArguments(ClickEventArguments):
    type: Literal['dragstart', 'dragend']
    object_id: str
    object_name: str
    x: float
    y: float
    z: float


@dataclass(**KWONLY_SLOTS)
class ColorPickEventArguments(UiEventArguments):
    color: str


@dataclass(**KWONLY_SLOTS)
class MouseEventArguments(UiEventArguments):
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
class JoystickEventArguments(UiEventArguments):
    action: str
    x: float | None = None
    y: float | None = None


@dataclass(**KWONLY_SLOTS)
class UploadEventArguments(UiEventArguments):
    file: FileUpload


@dataclass(**KWONLY_SLOTS)
class MultiUploadEventArguments(UiEventArguments):
    files: list[FileUpload]


@dataclass(**KWONLY_SLOTS)
class ValueChangeEventArguments(UiEventArguments):
    value: Any
    previous_value: Any = ...

    def __post_init__(self):
        # DEPRECATED: previous_value will be required in NiceGUI 4.0
        if self.previous_value is ...:
            helpers.warn_once('The new event argument `ValueChangeEventArguments.previous_value` is not set. '
                              'In NiceGUI 4.0 this will raise an error.')


@dataclass(**KWONLY_SLOTS)
class TableSelectionEventArguments(UiEventArguments):
    selection: list[Any]


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

    def __iter__(self) -> Iterator[bool]:
        return iter([self.alt, self.ctrl, self.meta, self.shift])

    def __len__(self) -> int:
        return sum(self)


@dataclass(**KWONLY_SLOTS)
class KeyboardKey:
    name: str
    code: str
    location: int

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return other in {self.name, self.code}
        if isinstance(other, KeyboardKey):
            return (self.name, self.code, self.location) == (other.name, other.code, other.location)
        return False

    def __hash__(self) -> int:
        return hash((self.name, self.code, self.location))

    def __repr__(self):
        return str(self.name)

    @property
    def is_cursorkey(self) -> bool:
        """Whether the key is a cursor key (arrow keys)."""
        return self.code.startswith('Arrow')

    @property
    def number(self) -> int | None:
        """Integer value of a number key."""
        return int(self.code[len('Digit'):]) if self.code.startswith('Digit') else None

    @property
    def backspace(self) -> bool:
        """Whether the key is the backspace key."""
        return self.name == 'Backspace'

    @property
    def tab(self) -> bool:
        """Whether the key is the tab key."""
        return self.name == 'Tab'

    @property
    def enter(self) -> bool:
        """Whether the key is the enter key."""
        return self.name == 'Enter'

    @property
    def shift(self) -> bool:
        """Whether the key is the shift key."""
        return self.name == 'Shift'

    @property
    def control(self) -> bool:
        """Whether the key is the control key."""
        return self.name == 'Control'

    @property
    def alt(self) -> bool:
        """Whether the key is the alt key."""
        return self.name == 'Alt'

    @property
    def pause(self) -> bool:
        """Whether the key is the pause key."""
        return self.name == 'Pause'

    @property
    def caps_lock(self) -> bool:
        """Whether the key is the caps lock key."""
        return self.name == 'CapsLock'

    @property
    def escape(self) -> bool:
        """Whether the key is the escape key."""
        return self.name == 'Escape'

    @property
    def space(self) -> bool:
        """Whether the key is the space key."""
        return self.name == ' '

    @property
    def page_up(self) -> bool:
        """Whether the key is the page up key."""
        return self.name == 'PageUp'

    @property
    def page_down(self) -> bool:
        """Whether the key is the page down key."""
        return self.name == 'PageDown'

    @property
    def end(self) -> bool:
        """Whether the key is the end key."""
        return self.name == 'End'

    @property
    def home(self) -> bool:
        """Whether the key is the home key."""
        return self.name == 'Home'

    @property
    def arrow_left(self) -> bool:
        """Whether the key is the arrow left key."""
        return self.name == 'ArrowLeft'

    @property
    def arrow_up(self) -> bool:
        """Whether the key is the arrow up key."""
        return self.name == 'ArrowUp'

    @property
    def arrow_right(self) -> bool:
        """Whether the key is the arrow right key."""
        return self.name == 'ArrowRight'

    @property
    def arrow_down(self) -> bool:
        """Whether the key is the arrow down key."""
        return self.name == 'ArrowDown'

    @property
    def print_screen(self) -> bool:
        """Whether the key is the print screen key."""
        return self.name == 'PrintScreen'

    @property
    def insert(self) -> bool:
        """Whether the key is the insert key."""
        return self.name == 'Insert'

    @property
    def delete(self) -> bool:
        """Whether the key is the delete key."""
        return self.name == 'Delete'

    @property
    def meta(self) -> bool:
        """Whether the key is the meta key."""
        return self.name == 'Meta'

    @property
    def f1(self) -> bool:
        """Whether the key is the F1 key."""
        return self.name == 'F1'

    @property
    def f2(self) -> bool:
        """Whether the key is the F2 key."""
        return self.name == 'F2'

    @property
    def f3(self) -> bool:
        """Whether the key is the F3 key."""
        return self.name == 'F3'

    @property
    def f4(self) -> bool:
        """Whether the key is the F4 key."""
        return self.name == 'F4'

    @property
    def f5(self) -> bool:
        """Whether the key is the F5 key."""
        return self.name == 'F5'

    @property
    def f6(self) -> bool:
        """Whether the key is the F6 key."""
        return self.name == 'F6'

    @property
    def f7(self) -> bool:
        """Whether the key is the F7 key."""
        return self.name == 'F7'

    @property
    def f8(self) -> bool:
        """Whether the key is the F8 key."""
        return self.name == 'F8'

    @property
    def f9(self) -> bool:
        """Whether the key is the F9 key."""
        return self.name == 'F9'

    @property
    def f10(self) -> bool:
        """Whether the key is the F10 key."""
        return self.name == 'F10'

    @property
    def f11(self) -> bool:
        """Whether the key is the F11 key."""
        return self.name == 'F11'

    @property
    def f12(self) -> bool:
        """Whether the key is the F12 key."""
        return self.name == 'F12'


@dataclass(**KWONLY_SLOTS)
class KeyEventArguments(UiEventArguments):
    action: KeyboardAction
    key: KeyboardKey
    modifiers: KeyboardModifiers


@dataclass(**KWONLY_SLOTS)
class ScrollEventArguments(UiEventArguments):
    vertical_position: float
    vertical_percentage: float
    vertical_size: float
    vertical_container_size: float
    horizontal_position: float
    horizontal_percentage: float
    horizontal_size: float
    horizontal_container_size: float


@dataclass(**KWONLY_SLOTS)
class JsonEditorSelectEventArguments(UiEventArguments):
    selection: dict


@dataclass(**KWONLY_SLOTS)
class JsonEditorChangeEventArguments(UiEventArguments):
    content: dict
    errors: dict = field(default_factory=dict)


@dataclass(**KWONLY_SLOTS)
class XtermBellEventArguments(UiEventArguments):
    pass


@dataclass(**KWONLY_SLOTS)
class XtermDataEventArguments(UiEventArguments):
    data: str


EventT = TypeVar('EventT', bound=EventArguments)
Handler: TypeAlias = Callable[[EventT], Any] | Callable[[], Any]


def handle_event(handler: Handler[EventT] | None, arguments: EventT) -> None:
    """Call the given event handler.

    The handler is called within the context of the parent slot of the sender.
    If the handler is a coroutine, it is scheduled as a background task.
    If the handler expects arguments, the arguments are passed to the handler.
    Exceptions are caught and handled globally.

    :param handler: the event handler
    :param arguments: the event arguments
    """
    if handler is None:
        return
    try:
        parent_slot: Slot | nullcontext
        if isinstance(arguments, UiEventArguments):
            parent_slot = arguments.sender.parent_slot or arguments.sender.client.layout.default_slot
        else:
            parent_slot = nullcontext()

        with parent_slot:
            if helpers.expects_arguments(handler):
                result = cast(Callable[[EventT], Any], handler)(arguments)
            else:
                result = cast(Callable[[], Any], handler)()
        if isinstance(result, Awaitable) and not isinstance(result, AwaitableResponse) and not isinstance(result, asyncio.Task):
            # NOTE: await an awaitable result even if the handler is not a coroutine (like a lambda statement)
            async def wait_for_result():
                with parent_slot:
                    try:
                        await result
                    except Exception as e:
                        core.app.handle_exception(e)
            if core.loop and core.loop.is_running():
                background_tasks.create(wait_for_result(), name=str(handler))
            else:
                core.app.on_startup(wait_for_result())
    except Exception as e:
        core.app.handle_exception(e)
