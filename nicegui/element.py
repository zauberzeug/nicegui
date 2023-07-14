from __future__ import annotations

import inspect
import re
from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterator, List, Optional, Union

from typing_extensions import Self

from nicegui import json

from . import binding, events, globals, outbox, storage
from .dependencies import JsComponent, Library, register_library, register_vue_component
from .elements.mixins.visibility import Visibility
from .event_listener import EventListener
from .slot import Slot
from .tailwind import Tailwind

if TYPE_CHECKING:
    from .client import Client

PROPS_PATTERN = re.compile(r'([:\w\-]+)(?:=(?:("[^"\\]*(?:\\.[^"\\]*)*")|([\w\-.%:\/]+)))?(?:$|\s)')


class Element(Visibility):
    component: Optional[JsComponent] = None
    libraries: List[Library] = []
    extra_libraries: List[Library] = []
    exposed_libraries: List[Library] = []

    def __init__(self, tag: Optional[str] = None, *, _client: Optional[Client] = None) -> None:
        """Generic Element

        This class is the base class for all other UI elements.
        But you can use it to create elements with arbitrary HTML tags.

        :param tag: HTML tag of the element
        :param _client: client for this element (for internal use only)
        """
        super().__init__()
        self.client = _client or globals.get_client()
        self.id = self.client.next_element_id
        self.client.next_element_id += 1
        self.tag = tag if tag else self.component.tag if self.component else 'div'
        self._classes: List[str] = []
        self._style: Dict[str, str] = {}
        self._props: Dict[str, Any] = {'key': self.id}  # HACK: workaround for #600 and #898
        self._event_listeners: Dict[str, EventListener] = {}
        self._text: Optional[str] = None
        self.slots: Dict[str, Slot] = {}
        self.default_slot = self.add_slot('default')

        self.client.elements[self.id] = self
        self.parent_slot: Optional[Slot] = None
        slot_stack = globals.get_slot_stack()
        if slot_stack:
            self.parent_slot = slot_stack[-1]
            self.parent_slot.children.append(self)

        self.tailwind = Tailwind(self)

        outbox.enqueue_update(self)
        if self.parent_slot:
            outbox.enqueue_update(self.parent_slot.parent)

    def __init_subclass__(cls, *,
                          component: Union[str, Path, None] = None,
                          libraries: List[Union[str, Path]] = [],
                          exposed_libraries: List[Union[str, Path]] = [],
                          extra_libraries: List[Union[str, Path]] = [],
                          ) -> None:
        super().__init_subclass__()
        base = Path(inspect.getfile(cls)).parent

        def glob_absolute_paths(file: Union[str, Path]) -> List[Path]:
            path = Path(file)
            if not path.is_absolute():
                path = base / path
            return sorted(path.parent.glob(path.name), key=lambda p: p.stem)

        cls.component = None
        if component:
            for path in glob_absolute_paths(component):
                cls.component = register_vue_component(path)

        cls.libraries = []
        for library in libraries:
            for path in glob_absolute_paths(library):
                cls.libraries.append(register_library(path))

        cls.extra_libraries = []
        for library in extra_libraries:
            for path in glob_absolute_paths(library):
                cls.extra_libraries.append(register_library(path))

        cls.exposed_libraries = []
        for library in exposed_libraries:
            for path in glob_absolute_paths(library):
                cls.exposed_libraries.append(register_library(path, expose=True))

    def add_slot(self, name: str, template: Optional[str] = None) -> Slot:
        """Add a slot to the element.

        :param name: name of the slot
        :param template: Vue template of the slot
        :return: the slot
        """
        self.slots[name] = Slot(self, name, template)
        return self.slots[name]

    def __enter__(self) -> Self:
        self.default_slot.__enter__()
        return self

    def __exit__(self, *_):
        self.default_slot.__exit__(*_)

    def __iter__(self) -> Iterator[Element]:
        for slot in self.slots.values():
            for child in slot:
                yield child

    def _collect_slot_dict(self) -> Dict[str, Any]:
        return {
            name: {'template': slot.template, 'ids': [child.id for child in slot]}
            for name, slot in self.slots.items()
        }

    def _to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'tag': self.tag,
            'class': self._classes,
            'style': self._style,
            'props': self._props,
            'text': self._text,
            'slots': self._collect_slot_dict(),
            'events': [listener.to_dict() for listener in self._event_listeners.values()],
            'component': {
                'key': self.component.key,
                'name': self.component.name,
                'tag': self.component.tag
            } if self.component else None,
            'libraries': [
                {
                    'key': library.key,
                    'name': library.name,
                } for library in self.libraries
            ],
        }

    @staticmethod
    def _update_classes_list(
            classes: List[str],
            add: Optional[str] = None, remove: Optional[str] = None, replace: Optional[str] = None) -> List[str]:
        class_list = classes if replace is None else []
        class_list = [c for c in class_list if c not in (remove or '').split()]
        class_list += (add or '').split()
        class_list += (replace or '').split()
        return list(dict.fromkeys(class_list))  # NOTE: remove duplicates while preserving order

    def classes(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None) \
            -> Self:
        """Apply, remove, or replace HTML classes.

        This allows modifying the look of the element or its layout using `Tailwind <https://tailwindcss.com/>`_ or `Quasar <https://quasar.dev/>`_ classes.

        Removing or replacing classes can be helpful if predefined classes are not desired.

        :param add: whitespace-delimited string of classes
        :param remove: whitespace-delimited string of classes to remove from the element
        :param replace: whitespace-delimited string of classes to use instead of existing ones
        """
        new_classes = self._update_classes_list(self._classes, add, remove, replace)
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

    def style(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None) -> Self:
        """Apply, remove, or replace CSS definitions.

        Removing or replacing styles can be helpful if the predefined style is not desired.

        :param add: semicolon-separated list of styles to add to the element
        :param remove: semicolon-separated list of styles to remove from the element
        :param replace: semicolon-separated list of styles to use instead of existing ones
        """
        style_dict = deepcopy(self._style) if replace is None else {}
        for key in self._parse_style(remove):
            style_dict.pop(key, None)
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
        """Add or remove props.

        This allows modifying the look of the element or its layout using `Quasar <https://quasar.dev/>`_ props.
        Since props are simply applied as HTML attributes, they can be used with any HTML element.

        Boolean properties are assumed ``True`` if no value is specified.

        :param add: whitespace-delimited list of either boolean values or key=value pair to add
        :param remove: whitespace-delimited list of property keys to remove
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
        """Add a tooltip to the element.

        :param text: text of the tooltip
        """
        with self:
            tooltip = Element('q-tooltip')
            tooltip._text = text
        return self

    def on(self,
           type: str,
           handler: Optional[Callable[..., Any]] = None,
           args: Optional[List[str]] = None, *,
           throttle: float = 0.0,
           leading_events: bool = True,
           trailing_events: bool = True,
           ) -> Self:
        """Subscribe to an event.

        :param type: name of the event (e.g. "click", "mousedown", or "update:model-value")
        :param handler: callback that is called upon occurrence of the event
        :param args: arguments included in the event message sent to the event handler (default: `None` meaning all)
        :param throttle: minimum time (in seconds) between event occurrences (default: 0.0)
        :param leading_events: whether to trigger the event handler immediately upon the first event occurrence (default: `True`)
        :param trailing_events: whether to trigger the event handler after the last event occurrence (default: `True`)
        """
        if handler:
            listener = EventListener(
                element_id=self.id,
                type=type,
                args=[args] if args and isinstance(args[0], str) else args,
                handler=handler,
                throttle=throttle,
                leading_events=leading_events,
                trailing_events=trailing_events,
                request=storage.request_contextvar.get(),
            )
            self._event_listeners[listener.id] = listener
            self.update()
        return self

    def _handle_event(self, msg: Dict) -> None:
        listener = self._event_listeners[msg['listener_id']]
        storage.request_contextvar.set(listener.request)
        args = events.GenericEventArguments(sender=self, client=self.client, args=msg['args'])
        events.handle_event(listener.handler, args)

    def update(self) -> None:
        """Update the element on the client side."""
        outbox.enqueue_update(self)

    def run_method(self, name: str, *args: Any) -> None:
        """Run a method on the client side.

        :param name: name of the method
        :param args: arguments to pass to the method
        """
        if not globals.loop:
            return
        data = {'id': self.id, 'name': name, 'args': args}
        outbox.enqueue_message('run_method', data, globals._socket_id or self.client.id)

    def _collect_descendant_ids(self) -> List[int]:
        ids: List[int] = [self.id]
        for child in self:
            ids.extend(child._collect_descendant_ids())
        return ids

    def clear(self) -> None:
        """Remove all child elements."""
        descendants = [self.client.elements[id] for id in self._collect_descendant_ids()[1:]]
        binding.remove(descendants, Element)
        for element in descendants:
            element.delete()
            del self.client.elements[element.id]
        for slot in self.slots.values():
            slot.children.clear()
        self.update()

    def move(self, target_container: Optional[Element] = None, target_index: int = -1):
        """Move the element to another container.

        :param target_container: container to move the element to (default: the parent container)
        :param target_index: index within the target slot (default: append to the end)
        """
        assert self.parent_slot is not None
        self.parent_slot.children.remove(self)
        self.parent_slot.parent.update()
        target_container = target_container or self.parent_slot.parent
        target_index = target_index if target_index >= 0 else len(target_container.default_slot.children)
        target_container.default_slot.children.insert(target_index, self)
        self.parent_slot = target_container.default_slot
        target_container.update()

    def remove(self, element: Union[Element, int]) -> None:
        """Remove a child element.

        :param element: either the element instance or its ID
        """
        if isinstance(element, int):
            children = list(self)
            element = children[element]
        binding.remove([element], Element)
        element.delete()
        del self.client.elements[element.id]
        for slot in self.slots.values():
            slot.children[:] = [e for e in slot if e.id != element.id]
        self.update()

    def delete(self) -> None:
        """Perform cleanup when the element is deleted."""
        outbox.enqueue_delete(self)
