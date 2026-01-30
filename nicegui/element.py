from __future__ import annotations

import inspect
import re
import weakref
from collections.abc import Callable, Iterator, Sequence
from copy import copy
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, cast

from typing_extensions import Self

from . import core, events, helpers, json, storage
from .awaitable_response import AwaitableResponse, NullResponse
from .classes import Classes
from .context import context
from .dependencies import (
    Component,
    Library,
    register_dynamic_resource,
    register_esm,
    register_library,
    register_resource,
    register_vue_component,
)
from .elements.mixins.visibility import Visibility
from .event_listener import EventListener
from .props import Props
from .slot import Slot
from .style import Style
from .version import __version__

if TYPE_CHECKING:
    from .client import Client

# https://www.w3.org/TR/xml/#sec-common-syn
TAG_START_CHAR = r':|[A-Z]|_|[a-z]|[\u00C0-\u00D6]|[\u00D8-\u00F6]|[\u00F8-\u02FF]|[\u0370-\u037D]|[\u037F-\u1FFF]|[\u200C-\u200D]|[\u2070-\u218F]|[\u2C00-\u2FEF]|[\u3001-\uD7FF]|[\uF900-\uFDCF]|[\uFDF0-\uFFFD]|[\U00010000-\U000EFFFF]'
TAG_CHAR = TAG_START_CHAR + r'|-|\.|[0-9]|\u00B7|[\u0300-\u036F]|[\u203F-\u2040]'
TAG_PATTERN = re.compile(fr'^({TAG_START_CHAR})({TAG_CHAR})*$')


class Element(Visibility):
    component: Component | None = None
    exposed_libraries: ClassVar[list[Library]] = []
    _default_props: ClassVar[dict[str, Any]] = {}
    _default_classes: ClassVar[list[str]] = []
    _default_style: ClassVar[dict[str, str]] = {}

    def __init__(self, tag: str | None = None, *, _client: Client | None = None) -> None:
        """Generic Element

        This class is the base class for all other UI elements.
        But you can use it to create elements with arbitrary HTML tags.

        :param tag: HTML tag of the element
        :param _client: client for this element (for internal use only)
        """
        super().__init__()
        client = _client or context.client
        self._client = weakref.ref(client)
        self.id = client.next_element_id
        client.next_element_id += 1
        self.tag = tag if tag else self.component.tag if self.component else 'div'
        if not TAG_PATTERN.match(self.tag):
            raise ValueError(f'Invalid HTML tag: {self.tag}')
        self._classes: Classes[Self] = Classes(self._default_classes, element=cast(Self, self))
        self._style: Style[Self] = Style(self._default_style, element=cast(Self, self))
        self._props: Props[Self] = Props(self._default_props, element=cast(Self, self))
        self._markers: list[str] = []
        self._event_listeners: dict[str, EventListener] = {}
        self._text: str | None = None
        self.slots: dict[str, Slot] = {}
        self.default_slot = self.add_slot('default')
        self._update_method: str | None = None
        self._deleted: bool = False

        client.elements[self.id] = self
        self._parent_slot: weakref.ref[Slot] | None = None
        slot_stack = context.slot_stack
        if slot_stack:
            parent_slot = slot_stack[-1]
            parent_slot.children.append(self)
            self._parent_slot = weakref.ref(parent_slot)

        client.outbox.enqueue_update(self)
        if self._parent_slot:
            client.outbox.enqueue_update(parent_slot.parent)

        self._props.add_rename('resource_path', 'resource-path')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('dynamic_resource_path', 'dynamic-resource-path')  # DEPRECATED: remove in NiceGUI 4.0

    def __init_subclass__(cls, *,
                          component: str | Path | None = None,
                          dependencies: list[str | Path] = [],  # noqa: B006
                          esm: dict[str, str] | None = None,
                          default_classes: str | None = None,
                          default_style: str | None = None,
                          default_props: str | None = None,
                          ) -> None:
        super().__init_subclass__()
        base = Path(inspect.getfile(cls)).parent

        def glob_absolute_paths(file: str | Path) -> list[Path]:
            path = Path(file)
            if not path.is_absolute():
                path = base / path
            return sorted(path.parent.glob(path.name), key=lambda p: p.stem)

        cls.component = copy(cls.component)
        cls.exposed_libraries = copy(cls.exposed_libraries)
        if component:
            max_time = max((path.stat().st_mtime for path in glob_absolute_paths(component)), default=None)
            for path in glob_absolute_paths(component):
                cls.component = register_vue_component(path, max_time=max_time)
        for library in dependencies:
            max_time = max((path.stat().st_mtime for path in glob_absolute_paths(library)), default=None)
            for path in glob_absolute_paths(library):
                cls.exposed_libraries.append(register_library(path, max_time=max_time))
        for key, esm_path in (esm or {}).items():
            path = Path(esm_path)
            if not path.is_absolute():
                path = base / path
            max_time = max((path.stat().st_mtime for path in glob_absolute_paths(path)), default=None)
            register_esm(key, path, max_time=max_time)

        cls._default_props = copy(cls._default_props)
        cls._default_classes = copy(cls._default_classes)
        cls._default_style = copy(cls._default_style)
        cls.default_classes(default_classes)
        cls.default_style(default_style)
        cls.default_props(default_props)

    @property
    def client(self) -> Client:
        """The client this element belongs to."""
        client = self._client()
        if client is None:
            raise RuntimeError('The client this element belongs to has been deleted.')
        return client

    @property
    def parent_slot(self) -> Slot | None:
        """The parent slot of the element."""
        if self._parent_slot is None:
            return None
        parent_slot = self._parent_slot()
        if parent_slot is None:
            raise RuntimeError('The parent slot of the element has been deleted.')
        return parent_slot

    @parent_slot.setter
    def parent_slot(self, value: Slot | None) -> None:
        self._parent_slot = weakref.ref(value) if value else None

    def add_resource(self, path: str | Path) -> None:
        """Add a resource to the element.

        :param path: path to the resource (e.g. folder with CSS and JavaScript files)
        """
        path_ = Path(path)
        resource = register_resource(path_, max_time=path_.stat().st_mtime)
        self._props['resource-path'] = f'/_nicegui/{__version__}/resources/{resource.key}'

    def add_dynamic_resource(self, name: str, function: Callable) -> None:
        """Add a dynamic resource to the element which returns the result of a function.

        :param name: name of the resource
        :param function: function that returns the resource response
        """
        register_dynamic_resource(name, function)
        self._props['dynamic-resource-path'] = f'/_nicegui/{__version__}/dynamic_resources'

    def add_slot(self, name: str, template: str | None = None) -> Slot:
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
            yield from slot

    def _collect_slot_dict(self) -> dict[str, Any]:
        return {
            name: {
                'ids': [child.id for child in slot],
                **({'template': slot.template} if slot.template is not None else {}),
            }
            for name, slot in self.slots.items()
            if slot != self.default_slot
        }

    def _to_dict(self) -> dict[str, Any]:
        return {
            'tag': self.tag,
            **({'text': self._text} if self._text is not None else {}),
            **{
                key: value
                for key, value in {
                    'class': self._classes,
                    'style': self._style,
                    'props': self._props,
                    'slots': self._collect_slot_dict(),
                    'children': [child.id for child in self.default_slot.children],
                    'events': [listener.to_dict() for listener in self._event_listeners.values()],
                    'update_method': self._update_method,
                }.items()
                if value
            },
        }

    @property
    def classes(self) -> Classes[Self]:
        """The classes of the element."""
        return self._classes

    @classmethod
    def default_classes(cls,
                        add: str | None = None, *,
                        remove: str | None = None,
                        toggle: str | None = None,
                        replace: str | None = None) -> type[Self]:
        """Apply, remove, toggle, or replace default HTML classes.

        This allows modifying the look of the element or its layout using `Tailwind <https://tailwindcss.com/>`_ or `Quasar <https://quasar.dev/>`_ classes.

        Removing or replacing classes can be helpful if predefined classes are not desired.
        All elements of this class will share these HTML classes.
        These must be defined before element instantiation.

        :param add: whitespace-delimited string of classes
        :param remove: whitespace-delimited string of classes to remove from the element
        :param toggle: whitespace-delimited string of classes to toggle (*added in version 2.7.0*)
        :param replace: whitespace-delimited string of classes to use instead of existing ones
        """
        cls._default_classes = Classes.update_list(cls._default_classes, add, remove, toggle, replace)
        return cls

    @property
    def style(self) -> Style[Self]:
        """The style of the element."""
        return self._style

    @classmethod
    def default_style(cls,
                      add: str | None = None, *,
                      remove: str | None = None,
                      replace: str | None = None) -> type[Self]:
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
        for key in Style.parse(remove):
            cls._default_style.pop(key, None)
        cls._default_style.update(Style.parse(add))
        cls._default_style.update(Style.parse(replace))
        return cls

    @property
    def props(self) -> Props[Self]:
        """The props of the element."""
        return self._props

    @classmethod
    def default_props(cls,
                      add: str | None = None, *,
                      remove: str | None = None) -> type[Self]:
        """Add or remove default props.

        This allows modifying the look of the element or its layout using `Quasar <https://quasar.dev/>`_ props.
        Since props are simply applied as HTML attributes, they can be used with any HTML element.
        All elements of this class will share these props.
        These must be defined before element instantiation.

        Boolean properties are assumed ``True`` if no value is specified.

        :param add: whitespace-delimited list of either boolean values or key=value pair to add
        :param remove: whitespace-delimited list of property keys to remove
        """
        for key in Props.parse(remove):
            if key in cls._default_props:
                del cls._default_props[key]
        for key, value in Props.parse(add).items():
            cls._default_props[key] = value
        return cls

    def mark(self, *markers: str) -> Self:
        """Replace markers of the element.

        Markers are used to identify elements for querying with `ElementFilter </documentation/element_filter>`_
        which is heavily used in testing
        but can also be used to reduce the number of global variables or passing around dependencies.

        :param markers: list of strings or single string with whitespace-delimited markers; replaces existing markers
        """
        self._markers = [word for marker in markers for word in marker.split()]
        return self

    def tooltip(self, text: str) -> Self:
        """Add a tooltip to the element.

        :param text: text of the tooltip
        """
        from .elements.tooltip import Tooltip  # pylint: disable=import-outside-toplevel, cyclic-import
        Tooltip(text).props['target'] = f'#{self.html_id}'
        return self

    def on(self,
           type: str,  # pylint: disable=redefined-builtin
           handler: events.Handler[events.GenericEventArguments] | None = None,
           args: None | Sequence[str] | Sequence[Sequence[str] | None] = None,
           *,
           throttle: float = 0.0,
           leading_events: bool = True,
           trailing_events: bool = True,
           js_handler: str = '(...args) => emit(...args)',
           ) -> Self:
        """Subscribe to an event.

        The event handler can be a Python function, a JavaScript function or a combination of both:

        - If you want to handle the event on the server with all (serializable) event arguments,
          use a Python ``handler``.
        - If you want to handle the event on the client side without emitting anything to the server,
          use ``js_handler`` with a JavaScript function handling the event.
        - If you want to handle the event on the server with a subset or transformed version of the event arguments,
          use ``js_handler`` with a JavaScript function emitting the transformed arguments using ``emit()``, and
          use a Python ``handler`` to handle these arguments on the server side.
          The ``js_handler`` can also decide to selectively emit arguments to the server,
          in which case the Python ``handler`` will not always be called.

        Note that the arguments ``throttle``, ``leading_events``, and ``trailing_events`` are only relevant
        when emitting events to the server.

        *Updated in version 2.18.0: Both handlers can be specified at the same time.*

        :param type: name of the event (e.g. "click", "mousedown", or "update:model-value")
        :param handler: callback that is called upon occurrence of the event
        :param args: arguments included in the event message sent to the event handler (default: ``None`` meaning all)
        :param throttle: minimum time (in seconds) between event occurrences (default: 0.0)
        :param leading_events: whether to trigger the event handler immediately upon the first event occurrence (default: ``True``)
        :param trailing_events: whether to trigger the event handler after the last event occurrence (default: ``True``)
        :param js_handler: JavaScript function that is handling the event on the client (default: "(...args) => emit(...args)")
        """
        if handler or js_handler:
            listener = EventListener(
                element_id=self.id,
                type=helpers.event_type_to_camel_case(type),
                args=[args] if args and isinstance(args[0], str) else args,  # type: ignore
                handler=handler,
                js_handler=None if js_handler == '(...args) => emit(...args)' else js_handler,
                throttle=throttle,
                leading_events=leading_events,
                trailing_events=trailing_events,
                request=storage.request_contextvar.get(),
            )
            self._event_listeners[listener.id] = listener
            self.update()
        return self

    def _handle_event(self, msg: dict) -> None:
        listener = self._event_listeners[msg['listener_id']]
        storage.request_contextvar.set(listener.request)
        args = events.GenericEventArguments(sender=self, client=self.client, args=msg['args'])
        events.handle_event(listener.handler, args)

    def update(self) -> None:
        """Update the element on the client side."""
        if self.is_deleted:
            return
        self.client.outbox.enqueue_update(self)

    def run_method(self, name: str, *args: Any, timeout: float = 1) -> AwaitableResponse:
        """Run a method on the client side.

        If the function is awaited, the result of the method call is returned.
        Otherwise, the method is executed without waiting for a response.

        :param name: name of the method
        :param args: arguments to pass to the method
        :param timeout: maximum time to wait for a response (default: 1 second)
        """
        if not core.loop:
            return NullResponse()
        return self.client.run_javascript(f'return runMethod({self.id}, "{name}", {json.dumps(args)})', timeout=timeout)

    def get_computed_prop(self, prop_name: str, *, timeout: float = 1) -> AwaitableResponse:
        """Return a computed property.

        This function should be awaited so that the computed property is properly returned.

        :param prop_name: name of the computed prop
        :param timeout: maximum time to wait for a response (default: 1 second)
        """
        if not core.loop:
            return NullResponse()
        return self.client.run_javascript(f'return getComputedProp({self.id}, "{prop_name}")', timeout=timeout)

    def ancestors(self, *, include_self: bool = False) -> Iterator[Element]:
        """Iterate over the ancestors of the element.

        :param include_self: whether to include the element itself in the iteration
        """
        if include_self:
            yield self
        parent_slot = self.parent_slot
        if parent_slot:
            yield from parent_slot.parent.ancestors(include_self=True)

    def descendants(self, *, include_self: bool = False) -> Iterator[Element]:
        """Iterate over the descendants of the element.

        :param include_self: whether to include the element itself in the iteration
        """
        if include_self:
            yield self
        for child in self:
            yield from child.descendants(include_self=True)

    def clear(self) -> Self:
        """Remove all child elements."""
        self.client.remove_elements(self.descendants())
        for slot in self.slots.values():
            slot.children.clear()
        self.update()
        return self

    def move(self,
             target_container: Element | None = None,
             target_index: int = -1, *,
             target_slot: str | None = None) -> None:
        """Move the element to another container.

        :param target_container: container to move the element to (default: the parent container)
        :param target_index: index within the target slot (default: append to the end)
        :param target_slot: slot within the target container (default: default slot)
        """
        parent_slot = self.parent_slot
        assert parent_slot is not None
        parent_slot.children.remove(self)
        parent_slot.parent.update()
        target_container = target_container or parent_slot.parent

        if target_slot is None:
            parent_slot = target_container.default_slot
            self.parent_slot = parent_slot
        elif target_slot in target_container.slots:
            parent_slot = target_container.slots[target_slot]
            self.parent_slot = parent_slot
        else:
            raise ValueError(f'Slot "{target_slot}" does not exist in the target container. '
                             f'Add it first using `add_slot("{target_slot}")`.')

        target_index = target_index if target_index >= 0 else len(parent_slot.children)
        parent_slot.children.insert(target_index, self)

        target_container.update()

    def remove(self, element: Element | int) -> None:
        """Remove a child element.

        :param element: either the element instance or its ID
        """
        if isinstance(element, int):
            children = list(self)
            element = children[element]
        self.client.remove_elements(element.descendants(include_self=True))
        parent_slot = element.parent_slot
        assert parent_slot is not None
        parent_slot.children.remove(element)
        self.update()

    def delete(self) -> None:
        """Delete the element and all its children."""
        parent_slot = self.parent_slot
        assert parent_slot is not None
        parent_slot.parent.remove(self)

    def _handle_delete(self) -> None:
        """Called when the element is deleted.

        This method can be overridden in subclasses to perform cleanup tasks.
        """
        for slot in self.slots.values():
            slot.children.clear()
        self._event_listeners.clear()

    @property
    def is_deleted(self) -> bool:
        """Whether the element has been deleted."""
        return self._deleted

    def __str__(self) -> str:
        result = self.tag if type(self) is Element else self.__class__.__name__  # pylint: disable=unidiomatic-typecheck

        def shorten(content: Any, length: int = 20) -> str:
            text = str(content).replace('\n', ' ').replace('\r', ' ')
            return text[:length].strip() + '...' if len(text) > length else text

        additions = []
        if self._markers:
            additions.append(f'markers={", ".join(self._markers)}')
        if self._text:
            additions.append(f'text={shorten(self._text)}')
        if hasattr(self, 'content') and self.content:  # pylint: disable=no-member
            additions.append(f'content={shorten(self.content)}')  # pylint: disable=no-member
        IGNORED_PROPS = {'loopback', 'color', 'view', 'innerHTML', 'dynamic-resource-path'}
        additions += [
            f'{key}={shorten(value)}'
            for key, value in self._props.items()
            if not key.startswith('_') and key not in IGNORED_PROPS and value
        ]
        if not self.visible:
            additions.append(f'visible={self.visible}')
        if additions:
            result += f' [{", ".join(additions)}]'

        for child in self.default_slot.children:
            for line in str(child).split('\n'):
                result += f'\n {line}'

        return result

    @property
    def html_id(self) -> str:
        """The ID of the element in the HTML DOM.

        *Added in version 2.16.0*
        """
        return f'c{self.id}'
