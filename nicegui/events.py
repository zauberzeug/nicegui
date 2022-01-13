import asyncio
from inspect import signature
from justpy.htmlcomponents import HTMLBaseComponent
from pydantic import BaseModel
import traceback
from typing import Any, Awaitable, Callable, List, Optional, Union

from .elements.element import Element
from .task_logger import create_task

class EventArguments(BaseModel):
    class Config:
        arbitrary_types_allowed = True
    sender: Element

class ClickEventArguments(EventArguments):
    pass

class UploadEventArguments(EventArguments):
    files: List[bytes]

class ValueChangeEventArguments(EventArguments):
    value: Any

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

class KeyEventArguments(EventArguments):
    class Config:
        arbitrary_types_allowed = True
    action: KeyboardAction
    key: KeyboardKey
    modifiers: KeyboardModifiers


def handle_event(handler: Optional[Union[Callable, Awaitable]],
                 arguments: EventArguments,
                 *,
                 update: Optional[HTMLBaseComponent] = None):
    try:
        if handler is None:
            return
        no_arguments = not signature(handler).parameters
        result = handler() if no_arguments else handler(arguments)
        if asyncio.iscoroutinefunction(handler):
            async def async_handler():
                try:
                    await result
                    if update is not None:
                        await update.update()
                except Exception:
                    traceback.print_exc()
            create_task(async_handler(), name=str(handler))
            return False
        else:
            return result
    except Exception:
        traceback.print_exc()
