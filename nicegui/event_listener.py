from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from fastapi import Request

_SPECIAL_EVENT_MODIFIERS = {'capture', 'once', 'passive'}
_EVENT_MODIFIERS = {'stop', 'prevent', 'self', 'ctrl', 'shift', 'alt', 'meta'}


@dataclass(kw_only=True, slots=True)
class EventListener:
    id: str
    element_id: int
    type: str
    args: Sequence[Sequence[str] | None]
    handler: Callable | None
    js_handler: str | None
    throttle: float
    leading_events: bool
    trailing_events: bool
    request: Request | None

    def to_dict(self) -> dict[str, Any]:
        """Return a dictionary representation of the event listener."""
        type_, _, words = self.type.partition('.')
        specials: list[str] = []
        modifiers: list[str] = []
        keys: list[str] = []
        if words:
            for word in words.split('.'):
                if word in _SPECIAL_EVENT_MODIFIERS:
                    specials.append(word)
                elif word in _EVENT_MODIFIERS:
                    modifiers.append(word)
                else:
                    keys.append(word)
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
