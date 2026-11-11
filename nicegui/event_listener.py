import uuid
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Any

from fastapi import Request


@dataclass(kw_only=True, slots=True)
class EventListener:
    id: str = field(init=False)
    element_id: int
    type: str
    args: Sequence[Sequence[str] | None]
    handler: Callable | None
    js_handler: str | None
    throttle: float
    leading_events: bool
    trailing_events: bool
    request: Request | None

    def __post_init__(self) -> None:
        self.id = str(uuid.uuid4())

    def to_dict(self) -> dict[str, Any]:
        """Return a dictionary representation of the event listener."""
        words = self.type.split('.')
        type_ = words.pop(0)
        specials = [w for w in words if w in {'capture', 'once', 'passive'}]
        modifier_names = {'stop', 'prevent', 'self', 'ctrl', 'shift', 'alt', 'meta', 'exact', 'middle'}
        if type_ not in {'keydown', 'keyup', 'keypress'}:
            # "left" and "right" are arrow keys on keyboard events, but mouse-button modifiers on all other events
            # (mirroring Vue's compiler-dom)
            modifier_names |= {'left', 'right'}
        modifiers = [w for w in words if w in modifier_names]
        keys = [w for w in words if w not in specials + modifiers]
        return {
            'listener_id': self.id,
            'type': type_,
            'specials': specials,
            'modifiers': modifiers,
            'keys': keys,
            'args': self.args,
            'throttle': self.throttle,
            'leading_events': self.leading_events,
            'trailing_events': self.trailing_events,
            'js_handler': self.js_handler,
        }
