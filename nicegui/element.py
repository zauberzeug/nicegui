from __future__ import annotations

import shlex
from abc import ABC
from copy import deepcopy
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple, Union

from . import background_tasks, binding, globals
from .elements.mixins.visibility import Visibility
from .event_listener import EventListener
from .events import handle_event
from .slot import Slot

if TYPE_CHECKING:
    from .client import Client


class Element(ABC, Visibility):

    def __init__(self, tag: str, *, _client: Optional[Client] = None) -> None:
        super().__init__()
        self.client = _client or globals.get_client()
        self.id = self.client.next_element_id
        self.client.next_element_id += 1
        self.tag = tag
        self._classes: List[str] = []
        self._style: Dict[str, str] = {}
        self._props: Dict[str, Any] = {}
        self._event_listeners: List[EventListener] = []
        self._text: str = ''
        self.slots: Dict[str, Slot] = {}
        self.default_slot = self.add_slot('default')

        self.client.elements[self.id] = self
        self.parent_slot: Optional[Slot] = None
        slot_stack = globals.get_slot_stack()
        if slot_stack:
            self.parent_slot = slot_stack[-1]
            self.parent_slot.children.append(self)

    def add_slot(self, name: str) -> Slot:
        self.slots[name] = Slot(self, name)
        return self.slots[name]

    def __enter__(self):
        self.default_slot.__enter__()
        return self

    def __exit__(self, *_):
        self.default_slot.__exit__(*_)

    def to_dict(self) -> Dict:
        events: Dict[str, Dict] = {}
        for listener in self._event_listeners:
            words = listener.type.split('.')
            type = words.pop(0)
            specials = [w for w in words if w in {'capture', 'once', 'passive'}]
            modifiers = [w for w in words if w in {'stop', 'prevent', 'self', 'ctrl', 'shift', 'alt', 'meta'}]
            keys = [w for w in words if w not in specials + modifiers]
            events[listener.type] = {
                'listener_type': listener.type,
                'type': type,
                'specials': specials,
                'modifiers': modifiers,
                'keys': keys,
                'args': list(set(events.get(listener.type, {}).get('args', []) + listener.args)),
                'throttle': min(events.get(listener.type, {}).get('throttle', float('inf')), listener.throttle),
            }
        return {
            'id': self.id,
            'tag': self.tag,
            'class': self._classes,
            'style': self._style,
            'props': self._props,
            'events': events,
            'text': self._text,
            'slots': {name: [child.id for child in slot.children] for name, slot in self.slots.items()},
        }

    def classes(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None):
        '''HTML classes to modify the look of the element.
        Every class in the `remove` parameter will be removed from the element.
        Classes are separated with a blank space.
        This can be helpful if the predefined classes by NiceGUI are not wanted in a particular styling.
        '''
        class_list = self._classes if replace is None else []
        class_list = [c for c in class_list if c not in (remove or '').split()]
        class_list += (add or '').split()
        class_list += (replace or '').split()
        new_classes = list(dict.fromkeys(class_list))  # NOTE: remove duplicates while preserving order
        if self._classes != new_classes:
            self._classes = new_classes
            self.update()
        return self

    @staticmethod
    def _parse_style(text: Optional[str]) -> Dict[str, str]:
        return dict(_split(part, ':') for part in text.strip('; ').split(';')) if text else {}

    def style(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None):
        '''CSS style sheet definitions to modify the look of the element.
        Every style in the `remove` parameter will be removed from the element.
        Styles are separated with a semicolon.
        This can be helpful if the predefined style sheet definitions by NiceGUI are not wanted in a particular styling.
        '''
        style_dict = deepcopy(self._style) if replace is None else {}
        for key in self._parse_style(remove):
            if key in style_dict:
                del style_dict[key]
        style_dict.update(self._parse_style(add))
        style_dict.update(self._parse_style(replace))
        if self._style != style_dict:
            self._style = style_dict
            self.update()
        return self

    @staticmethod
    def _parse_props(text: Optional[str]) -> Dict[str, Any]:
        if not text:
            return {}
        lexer = shlex.shlex(text, posix=True)
        lexer.whitespace = ' '
        lexer.wordchars += '=-.%:/'
        return dict(_split(word, '=') if '=' in word else (word, True) for word in lexer)

    def props(self, add: Optional[str] = None, *, remove: Optional[str] = None):
        '''Quasar props https://quasar.dev/vue-components/button#design to modify the look of the element.
        Boolean props will automatically activated if they appear in the list of the `add` property.
        Props are separated with a blank space. String values must be quoted.
        Every prop passed to the `remove` parameter will be removed from the element.
        This can be helpful if the predefined props by NiceGUI are not wanted in a particular styling.
        '''
        needs_update = False
        for key in self._parse_props(remove):
            if key in self._props:
                needs_update = True
                del self._props[key]
        for key, value in self._parse_props(add).items():
            if self._props.get(key) != value:
                needs_update = True
                self._props[key] = value
        if needs_update:
            self.update()
        return self

    def tooltip(self, text: str):
        with self:
            tooltip = Element('q-tooltip')
            tooltip._text = text
        return self

    def on(self, type: str, handler: Optional[Callable], args: Optional[List[str]] = None, *, throttle: float = 0.0):
        if handler:
            args = args if args is not None else ['*']
            listener = EventListener(element_id=self.id, type=type, args=args, handler=handler, throttle=throttle)
            self._event_listeners.append(listener)
        return self

    def handle_event(self, msg: Dict) -> None:
        for listener in self._event_listeners:
            if listener.type == msg['type']:
                handle_event(listener.handler, msg, sender=self)

    def collect_descendant_ids(self) -> List[int]:
        '''includes own ID as first element'''
        ids: List[int] = [self.id]
        for slot in self.slots.values():
            for child in slot.children:
                ids.extend(child.collect_descendant_ids())
        return ids

    def update(self) -> None:
        if not globals.loop:
            return
        ids = self.collect_descendant_ids()
        elements = {id: self.client.elements[id].to_dict() for id in ids}
        background_tasks.create(globals.sio.emit('update', {'elements': elements}, room=self.client.id))

    def run_method(self, name: str, *args: Any) -> None:
        if not globals.loop:
            return
        data = {'id': self.id, 'name': name, 'args': args}
        background_tasks.create(globals.sio.emit('run_method', data, room=globals._socket_id or self.client.id))

    def clear(self) -> None:
        descendants = [self.client.elements[id] for id in self.collect_descendant_ids()[1:]]
        binding.remove(descendants, Element)
        for element in descendants:
            del self.client.elements[element.id]
        for slot in self.slots.values():
            slot.children.clear()
        self.update()

    def remove(self, element: Union[Element, int]) -> None:
        if isinstance(element, int):
            children = [child for slot in self.slots.values() for child in slot.children]
            element = children[element]
        binding.remove([element], Element)
        del self.client.elements[element.id]
        for slot in self.slots.values():
            slot.children[:] = [e for e in slot.children if e.id != element.id]
        self.update()

    def delete(self) -> None:
        """Called when the corresponding client is deleted.

        Can be overridden to perform cleanup.
        """


def _split(text: str, separator: str) -> Tuple[str, str]:
    words = text.split(separator, 1)
    return words[0].strip(), words[1].strip()
