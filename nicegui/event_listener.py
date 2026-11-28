from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Any

from fastapi import Request

# NOTE: nicegui.js restores these defaults in `replaceUndefinedAttributes`
_DEFAULTS: dict[str, Any] = {
    'specials': [],
    'modifiers': [],
    'keys': [],
    'args': None,
    'throttle': 0,
    'leading_events': True,
    'trailing_events': True,
    'js_handler': None,
}


@dataclass(kw_only=True, slots=True)
class EventListener:
    id: int
    element_id: int
    type: str
    args: Sequence[Sequence[str] | None] | None
    handler: Callable | None
    js_handler: str | None
    throttle: float
    leading_events: bool
    trailing_events: bool
    request: Request | None
    _dict: dict[str, Any] | None = field(default=None, init=False, repr=False, compare=False)

    def to_dict(self) -> dict[str, Any]:
        """Return a dictionary representation of the event listener.

        The result is computed once and reused for every serialization, so it must not be modified.
        """
        if self._dict is None:
            self._dict = self._build_dict()
        return self._dict

    def _build_dict(self) -> dict[str, Any]:
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
        listener_dict = {
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
        return {key: value for key, value in listener_dict.items() if key not in _DEFAULTS or value != _DEFAULTS[key]}
