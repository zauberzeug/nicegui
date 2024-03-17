from __future__ import annotations

import ast
import inspect
import re
from copy import copy, deepcopy
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterator, List, Optional, Sequence, Union, overload

from typing_extensions import Self

from . import context, core, events, helpers, json, storage
from .awaitable_response import AwaitableResponse, NullResponse
from .dependencies import Component, Library, register_library, register_resource, register_vue_component
from .elements.mixins.visibility import Visibility
from .event_listener import EventListener
from .slot import Slot
from .tailwind import Tailwind
from .version import __version__

if TYPE_CHECKING:
    from .client import Client

PROPS_PATTERN = re.compile(r'''
# Match a key-value pair optionally followed by whitespace or end of string
([:\w\-]+)          # Capture group 1: Key
(?:                 # Optional non-capturing group for value
    =               # Match the equal sign
    (?:             # Non-capturing group for value options
        (           # Capture group 2: Value enclosed in double quotes
            "       # Match  double quote
            [^"\\]* # Match any character except quotes or backslashes zero or more times
            (?:\\.[^"\\]*)*  # Match any escaped character followed by any character except quotes or backslashes zero or more times
            "       # Match the closing quote
        )
        |
        (           # Capture group 3: Value enclosed in single quotes
            '       # Match a single quote
            [^'\\]* # Match any character except quotes or backslashes zero or more times
            (?:\\.[^'\\]*)*  # Match any escaped character followed by any character except quotes or backslashes zero or more times
            '       # Match the closing quote
        )
        |           # Or
        ([\w\-.%:\/]+)  # Capture group 4: Value without quotes
    )
)?                  # End of optional non-capturing group for value
(?:$|\s)            # Match end of string or whitespace
''', re.VERBOSE)

# https://www.w3.org/TR/xml/#sec-common-syn
TAG_START_CHAR = r':|[A-Z]|_|[a-z]|[\u00C0-\u00D6]|[\u00D8-\u00F6]|[\u00F8-\u02FF]|[\u0370-\u037D]|[\u037F-\u1FFF]|[\u200C-\u200D]|[\u2070-\u218F]|[\u2C00-\u2FEF]|[\u3001-\uD7FF]|[\uF900-\uFDCF]|[\uFDF0-\uFFFD]|[\U00010000-\U000EFFFF]'
TAG_CHAR = TAG_START_CHAR + r'|-|\.|[0-9]|\u00B7|[\u0300-\u036F]|[\u203F-\u2040]'
TAG_PATTERN = re.compile(fr'^({TAG_START_CHAR})({TAG_CHAR})*$')


class Element(Visibility):
    component: Optional[Component] = None
    libraries: List[Library] = []
    extra_libraries: List[Library] = []
    exposed_libraries: List[Library] = []
    _default_props: Dict[str, Any] = {}
    _default_classes: List[str] = []
    _default_style: Dict[str, str] = {}

    def __init__(self, tag: Optional[str] = None, *, _client: Optional[Client] = None) -> None:
        """Generic Element

        This class is the base class for all other UI elements.
        But you can use it to create elements with arbitrary HTML tags.

        :param tag: HTML tag of the element
        :param _client: client for this element (for internal use only)
        """
        super().__init__()
        self.client = _client or context.get_client()
        self.id = self.client.next_element_id
        self.client.next_element_id += 1
        self.tag = tag if tag else self.component.tag if self.component else 'div'
        if not TAG_PATTERN.match(self.tag):
            raise ValueError(f'Invalid HTML tag: {self.tag}')
        self._classes: List[str] = []
        self._classes.extend(self._default_classes)
        self._style: Dict[str, str] = {}
        self._style.update(self._default_style)
        self._props: Dict[str, Any] = {'key': self.id}  # HACK: workaround for #600 and #898
        self._props.update(self._default_props)
        self._event_listeners: Dict[str, EventListener] = {}
        self._text: Optional[str] = None
        self.slots: Dict[str, Slot] = {}
        self.default_slot = self.add_slot('default')
        self._deleted: bool = False

        self.client.elements[self.id] = self
        self.parent_slot: Optional[Slot] = None
        slot_stack = context.get_slot_stack()
        if slot_stack:
            self.parent_slot = slot_stack[-1]
            self.parent_slot.children.append(self)

        self.tailwind = Tailwind(self)

        self.client.outbox.enqueue_update(self)
        if self.parent_slot:
            self.client.outbox.enqueue_update(self.parent_slot.parent)

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

        cls.component = copy(cls.component)
        cls.libraries = copy(cls.libraries)
        cls.extra_libraries = copy(cls.extra_libraries)
        cls.exposed_libraries = copy(cls.exposed_libraries)
        if component:
            for path in glob_absolute_paths(component):
                cls.component = register_vue_component(path)
        for library in libraries:
            for path in glob_absolute_paths(library):
                cls.libraries.append(register_library(path))
        for library in extra_libraries:
            for path in glob_absolute_paths(library):
                cls.extra_libraries.append(register_library(path))
        for library in exposed_libraries:
            for path in glob_absolute_paths(library):
                cls.exposed_libraries.append(register_library(path, expose=True))

        cls._default_props = copy(cls._default_props)
        cls._default_classes = copy(cls._default_classes)
        cls._default_style = copy(cls._default_style)

    def add_resource(self, path: Union[str, Path]) -> None:
        """Add a resource to the element.

        :param path: path to the resource (e.g. folder with CSS and JavaScript files)
        """
        resource = register_resource(Path(path))
        self._props['resource_path'] = f'/_nicegui/{__version__}/resources/{resource.key}'

    def add_slot(self, name: str, template: Optional[str] = None) -> Slot:
        """Add a slot to the element.

        NiceGUI is using the slot concept from Vue:
        Elements can have multiple slots, each possibly with a number of children.
        Most elements only have one slot, e.g. a `ui.card` (QCard) only has a default slot.
        But more complex elements like `ui.table` (QTable) can have more slots like "header", "body" and so on.
        If you nest NiceGUI elements via with `ui.row(): ...` you place new elements inside of the row's default slot.
        But if you use with `table.add_slot(...): ...`, you enter a different slot.

        The slot stack helps NiceGUI to keep track of which slot is currently used for new elements.
        The `parent` field holds a reference to its element.
        Whenever an element is entered via a `with` expression, its default slot is automatically entered as well.

        :param name: name of the slot
        :param template: Vue template of the slot
        :return: the slot
        """
        self.slots[name] = Slot(self, name, template)
        return self.slots[name]

    def __enter__(self) -> Self:
        self.default_slot.__enter__()
        return self

    def __exit__(self, *_) -> None:
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
    def _update_classes_list(classes: List[str],
                             add: Optional[str] = None,
                             remove: Optional[str] = None,
                             replace: Optional[str] = None) -> List[str]:
        class_list = classes if replace is None else []
        class_list = [c for c in class_list if c not in (remove or '').split()]
        class_list += (add or '').split()
        class_list += (replace or '').split()
        return list(dict.fromkeys(class_list))  # NOTE: remove duplicates while preserving order

    def classes(self,
                add: Optional[str] = None, *,
                remove: Optional[str] = None,
                replace: Optional[str] = None) -> Self:
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

    @classmethod
    def default_classes(cls,
                        add: Optional[str] = None, *,
                        remove: Optional[str] = None,
                        replace: Optional[str] = None) -> type[Self]:
        """Apply, remove, or replace default HTML classes.

        This allows modifying the look of the element or its layout using `Tailwind <https://tailwindcss.com/>`_ or `Quasar <https://quasar.dev/>`_ classes.

        Removing or replacing classes can be helpful if predefined classes are not desired.
        All elements of this class will share these HTML classes.
        These must be defined before element instantiation.

        :param add: whitespace-delimited string of classes
        :param remove: whitespace-delimited string of classes to remove from the element
        :param replace: whitespace-delimited string of classes to use instead of existing ones
        """
        cls._default_classes = cls._update_classes_list(cls._default_classes, add, remove, replace)
        return cls

    @staticmethod
    def _parse_style(text: Optional[str]) -> Dict[str, str]:
        result = {}
        for word in (text or '').split(';'):
            word = word.strip()
            if word:
                key, value = word.split(':', 1)
                result[key.strip()] = value.strip()
        return result

    def style(self,
              add: Optional[str] = None, *,
              remove: Optional[str] = None,
              replace: Optional[str] = None) -> Self:
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

    @classmethod
    def default_style(cls,
                      add: Optional[str] = None, *,
                      remove: Optional[str] = None,
                      replace: Optional[str] = None) -> type[Self]:
        """Apply, remove, or replace default CSS definitions.

        Removing or replacing styles can be helpful if the predefined style is not desired.
        All elements of this class will share these CSS definitions.
        These must be defined before element instantiation.

        :param add: semicolon-separated list of styles to add to the element
        :param remove: semicolon-separated list of styles to remove from the element
        :param replace: semicolon-separated list of styles to use instead of existing ones
        """
        if replace is not None:
            cls._default_style.clear()
        for key in cls._parse_style(remove):
            cls._default_style.pop(key, None)
        cls._default_style.update(cls._parse_style(add))
        cls._default_style.update(cls._parse_style(replace))
        return cls

    @staticmethod
    def _parse_props(text: Optional[str]) -> Dict[str, Any]:
        dictionary = {}
        for match in PROPS_PATTERN.finditer(text or ''):
            key = match.group(1)
            value = match.group(2) or match.group(3) or match.group(4)
            if value is None:
                dictionary[key] = True
            else:
                if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
                    value = ast.literal_eval(value)
                dictionary[key] = value
        return dictionary

    def props(self,
              add: Optional[str] = None, *,
              remove: Optional[str] = None) -> Self:
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

    @classmethod
    def default_props(cls,
                      add: Optional[str] = None, *,
                      remove: Optional[str] = None) -> type[Self]:
        """Add or remove default props.

        This allows modifying the look of the element or its layout using `Quasar <https://quasar.dev/>`_ props.
        Since props are simply applied as HTML attributes, they can be used with any HTML element.
        All elements of this class will share these props.
        These must be defined before element instantiation.

        Boolean properties are assumed ``True`` if no value is specified.

        :param add: whitespace-delimited list of either boolean values or key=value pair to add
        :param remove: whitespace-delimited list of property keys to remove
        """
        for key in cls._parse_props(remove):
            if key in cls._default_props:
                del cls._default_props[key]
        for key, value in cls._parse_props(add).items():
            cls._default_props[key] = value
        return cls

    def tooltip(self, text: str) -> Self:
        """Add a tooltip to the element.

        :param text: text of the tooltip
        """
        from .elements.tooltip import Tooltip  # pylint: disable=import-outside-toplevel, cyclic-import
        with self:
            Tooltip(text)
        return self

    @overload
    def on(self,
           type: str,  # pylint: disable=redefined-builtin
           *,
           js_handler: Optional[str] = None,
           ) -> Self:
        ...

    @overload
    def on(self,
           type: str,  # pylint: disable=redefined-builtin
           handler: Optional[Callable[..., Any]] = None,
           args: Union[None, Sequence[str], Sequence[Optional[Sequence[str]]]] = None,
           *,
           throttle: float = 0.0,
           leading_events: bool = True,
           trailing_events: bool = True,
           ) -> Self:
        ...

    def on(self,
           type: str,  # pylint: disable=redefined-builtin
           handler: Optional[Callable[..., Any]] = None,
           args: Union[None, Sequence[str], Sequence[Optional[Sequence[str]]]] = None,
           *,
           throttle: float = 0.0,
           leading_events: bool = True,
           trailing_events: bool = True,
           js_handler: Optional[str] = None,
           ) -> Self:
        """Subscribe to an event.

        :param type: name of the event (e.g. "click", "mousedown", or "update:model-value")
        :param handler: callback that is called upon occurrence of the event
        :param args: arguments included in the event message sent to the event handler (default: `None` meaning all)
        :param throttle: minimum time (in seconds) between event occurrences (default: 0.0)
        :param leading_events: whether to trigger the event handler immediately upon the first event occurrence (default: `True`)
        :param trailing_events: whether to trigger the event handler after the last event occurrence (default: `True`)
        :param js_handler: JavaScript code that is executed upon occurrence of the event, e.g. `(evt) => alert(evt)` (default: `None`)
        """
        if handler and js_handler:
            raise ValueError('Either handler or js_handler can be specified, but not both')

        if handler or js_handler:
            listener = EventListener(
                element_id=self.id,
                type=helpers.kebab_to_camel_case(type),
                args=[args] if args and isinstance(args[0], str) else args,  # type: ignore
                handler=handler,
                js_handler=js_handler,
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
        if self.is_deleted:
            return
        self.client.outbox.enqueue_update(self)

    def run_method(self, name: str, *args: Any, timeout: float = 1, check_interval: float = 0.01) -> AwaitableResponse:
        """Run a method on the client side.

        If the function is awaited, the result of the method call is returned.
        Otherwise, the method is executed without waiting for a response.

        :param name: name of the method
        :param args: arguments to pass to the method
        :param timeout: maximum time to wait for a response (default: 1 second)
        :param check_interval: time between checks for a response (default: 0.01 seconds)
        """
        if not core.loop:
            return NullResponse()
        return self.client.run_javascript(f'return runMethod({self.id}, "{name}", {json.dumps(args)})',
                                          timeout=timeout, check_interval=check_interval)

    def _collect_descendants(self, *, include_self: bool = False) -> List[Element]:
        elements: List[Element] = [self] if include_self else []
        for child in self:
            elements.extend(child._collect_descendants(include_self=True))  # pylint: disable=protected-access
        return elements

    def clear(self) -> None:
        """Remove all child elements."""
        descendants = self._collect_descendants()
        self.client.remove_elements(descendants)
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
        elements = element._collect_descendants(include_self=True)  # pylint: disable=protected-access
        self.client.remove_elements(elements)
        assert element.parent_slot is not None
        element.parent_slot.children.remove(element)
        self.update()

    def delete(self) -> None:
        """Delete the element and all its children."""
        assert self.parent_slot is not None
        self.parent_slot.parent.remove(self)

    def _handle_delete(self) -> None:
        """Called when the element is deleted.

        This method can be overridden in subclasses to perform cleanup tasks.
        """

    @property
    def is_deleted(self) -> bool:
        """Whether the element has been deleted."""
        return self._deleted
