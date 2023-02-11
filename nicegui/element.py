from __future__ import annotations

import json
import re
from abc import ABC
from copy import deepcopy
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Union

from . import background_tasks, binding, globals
from .elements.mixins.visibility import Visibility
from .event_listener import EventListener
from .events import handle_event
from .slot import Slot
from typing_extensions import Self

if TYPE_CHECKING:
    from .client import Client


PROPS_PATTERN = re.compile(r'([\w\-]+)(?:=(?:("[^"\\]*(?:\\.[^"\\]*)*")|([\w\-.%:\/]+)))?(?:$|\s)')


class Element(ABC, Visibility):
    """Define the base class for all html elements represented as Python objects.

    :param tag: The html tag (e.g. div, p, etc. of the element.)
    """

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

    def __enter__(self) -> Self:
        """Allow element to be used as a context manager (with statement.)"""
        self.default_slot.__enter__()
        return self

    def __exit__(self, *_):
        self.default_slot.__exit__(*_)

    def to_dict(self):
        """Get important attributes of an element as a dictionary."""
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

    def classes(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None) \
            -> Self:
        """Apply, remove, or replace HTML classes.

        Generally, this is for the purpose of modifying the look of the element or its layout, based on the
        Quasar framework.

        .. note:: Removing classes can be helpful if default NiceGUI class-styling is not desired.

        :param add: a white-space delimited string of classes
        :param remove: A white-space delimited string of classes to remove from the element.
        :param replace: A white-space delimited string of classes to use instead of existing.
        """
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
        result = {}
        for word in (text or '').split(';'):
            word = word.strip()
            if word:
                key, value = word.split(':', 1)
                result[key.strip()] = value.strip()
        return result

    def style(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None)\
            -> Self:
        """
        Apply, remove, or replace CSS style sheet definitions to modify the look of the element.

        .. note::
            Removing styles can be helpful if the predefined style sheet definitions by NiceGUI are not wanted
            in a particular styling.

        .. codeblock:: python

            my_btn=Button("MyButton).style("color: #6E93D6; font-size: 200%", remove="font-weight; background-color")

        :param add: A semicolon separated list of styles to add to the element.
        :param remove: A semicolon separated list of styles to remove from the element.
        :param replace: Like add, but existing styles will be replaced by given.
         """
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
        dictionary = {}
        for match in PROPS_PATTERN.finditer(text or ''):
            key = match.group(1)
            value = match.group(2) or match.group(3)
            if value and value.startswith('"') and value.endswith('"'):
                value = json.loads(value)
            dictionary[key] = value or True
        return dictionary

    def props(self, add: Optional[str] = None, *, remove: Optional[str] = None) -> Self:
        """Add or remove Quasar-specif properties to modify the look of the element.

        see https://quasar.dev/vue-components/button#design

        .. code:: python

            by_btn = Button("my_btn").props("outline icon=volume_up")

        .. note:: Boolean properties are assumed True by their existence.

        :param add: A whitespace separated list of either boolean values or key=value pair to add
        :param remove: A whitespace separated list of property keys to remove.
        """
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

    def tooltip(self, text: str) -> Self:
        with self:
            tooltip = Element('q-tooltip')
            tooltip._text = text
        return self

    def on(self, type: str, handler: Optional[Callable], args: Optional[List[str]] = None, *, throttle: float = 0.0) \
            -> Self:
        """Subscribe to any web or Quasar events available to an element.

        :param type: The name of the event sans the "on" prefix, e.g. "click", "mousedown"
        :param handler: The method that is called upon occurrence of the event.
        :param args: Additional arguments that should be passed to the event definition.
        :param throttle: Force a delay between events to limit frequency or bounce.
        """
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
        """
        Return a list of ids of the element and each of its descendents.

        .. note:: The first id in the list is that of the element.
        """
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
        """Remove all descendant (child) elements."""
        descendants = [self.client.elements[id] for id in self.collect_descendant_ids()[1:]]
        binding.remove(descendants, Element)
        for element in descendants:
            del self.client.elements[element.id]
        for slot in self.slots.values():
            slot.children.clear()
        self.update()

    def remove(self, element: Union[Element, int]) -> None:
        """
        Remove a descendant (child) element.

        :param element: Either the element instance or its id.
        """
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
