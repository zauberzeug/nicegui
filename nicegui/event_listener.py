from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from fastapi import Request


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
                if word in {'capture', 'once', 'passive'}:
                    specials.append(word)
                elif word in {'stop', 'prevent', 'self', 'ctrl', 'shift', 'alt', 'meta'}:
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
