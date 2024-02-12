import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional, Sequence

from fastapi import Request

from .dataclasses import KWONLY_SLOTS


def _type_to_dict(type_: str) -> Dict[str, Any]:
    """Convert a type string to a dictionary representation."""
    words = type_.split('.')
    type_ = words.pop(0)
    specials = [w for w in words if w in {'capture', 'once', 'passive'}]
    modifiers = [w for w in words if w in {'stop', 'prevent', 'self', 'ctrl', 'shift', 'alt', 'meta'}]
    keys = [w for w in words if w not in specials + modifiers]
    return {
        'type': type_,
        'specials': specials,
        'modifiers': modifiers,
        'keys': keys,
    }


@dataclass(**KWONLY_SLOTS)
class EventListener:
    id: str = field(init=False)
    element_id: int
    type: str
    args: Sequence[Optional[Sequence[str]]]
    handler: Callable
    throttle: float
    leading_events: bool
    trailing_events: bool
    request: Optional[Request]

    def __post_init__(self) -> None:
        self.id = str(uuid.uuid4())

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the event listener."""
        _dict = _type_to_dict(self.type)
        _dict.update({
            'listener_id': self.id,
            'args': self.args,
            'throttle': self.throttle,
            'leading_events': self.leading_events,
            'trailing_events': self.trailing_events,
        })
        return _dict


@dataclass(**KWONLY_SLOTS)
class JsEventListener:
    type: str
    js_handler: str

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the event listener."""
        _dict = _type_to_dict(self.type)
        _dict.update({
            'js_handler': self.js_handler,
        })
        return _dict
