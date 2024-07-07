
from __future__ import annotations

import asyncio
import re
from typing import List, Optional, Type, TypeVar, Union
from uuid import uuid4

import httpx
import socketio
from typing_extensions import Self

import nicegui.nicegui as ng
from nicegui import Client, ElementFilter, background_tasks, context, events, ui
from nicegui.element import Element
from nicegui.elements.mixins.value_element import ValueElement
from nicegui.logging import log

# pylint: disable=protected-access


T = TypeVar('T', bound=Element)


class User:
    current_user: Optional[User] = None

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.http_client = client
        self.sio = socketio.AsyncClient()
        self.client: Optional[Client] = None

    async def open(self, path: str) -> None:
        """Open the given path."""
        response = await self.http_client.get(path, follow_redirects=True)
        assert response.status_code == 200, f'Expected status code 200, got {response.status_code}'
        if response.headers.get('X-Nicegui-Content') != 'page':
            raise ValueError(f'Expected a page response, got {response.text}')

        match = re.search(r"'client_id': '([0-9a-f-]+)'", response.text)
        assert match is not None
        client_id = match.group(1)
        client = Client.instances[client_id]
        self.sio.on('connect')
        await ng._on_handshake(f'test-{uuid4()}', {'client_id': client.id, 'tab_id': str(uuid4())})
        self.client = client
        self.activate()

    def activate(self) -> Self:
        if self.current_user:
            self.current_user.deactivate()
        self.current_user = self
        assert self.client
        ui.navigate.to = lambda target, new_tab=False: background_tasks.create(self.open(target))
        self.client.__enter__()
        return self

    def deactivate(self, *_) -> None:
        assert self.client
        self.client.__exit__()
        msg = 'navigate.to unavailable in pytest simulation outside of an active client'
        ui.navigate.to = lambda target, new_tab=False: log.warning(msg)
        self.current_user = None

    async def should_see(self, *,
                         kind: Type[T] = Element,
                         marker: Union[str, list[str], None] = None,
                         content: Union[str, list[str], None] = None,
                         retries: int = 3,
                         ) -> ElementFilter:
        """Assert that the page contains an input with the given value."""
        assert self.client
        for _ in range(retries):
            with self.client:
                elements = ElementFilter(kind=kind, marker=marker, content=content)
                if len(elements) > 0:
                    return elements
                for m in context.client.outbox.messages:
                    if content is not None and m[1] == 'notify' and content in m[2]['message']:
                        return elements
                await asyncio.sleep(0.1)
        msg = f'expected to find an element of type {kind.__name__} with {marker=} and {content=} on the page:\n{self.current_page}'
        raise AssertionError(msg)

    async def should_not_see(self, *,
                             kind: Type[T] = Element,
                             marker: Union[str, list[str], None] = None,
                             content: Union[str, list[str], None] = None,
                             retries: int = 3,
                             ) -> None:
        """Assert that the page does not contain an input with the given value."""
        assert self.client
        for _ in range(retries):
            with self.client:
                elements = ElementFilter(kind=kind, marker=marker, content=content)
                if len(elements) == 0:
                    return
                await asyncio.sleep(0.1)
        msg = f'expected not to find an element of type {kind.__name__} with {marker=} and {content=} on the page:\n{self.current_page}'
        raise AssertionError(msg)

    async def type(self, text: str, *,
                   kind: Type[T] = ValueElement,
                   marker: Union[str, list[str], None] = None,
                   content: Union[str, list[str], None] = None,
                   ) -> None:
        """Type the given text into the input."""
        assert issubclass(kind, ValueElement)
        assert self.client
        with self.client:
            elements = await self.should_see(kind=kind, marker=marker, content=content)
            marker = f' with {marker=}' if marker is not None else ''
            assert len(elements) == 1, \
                f'expected to find exactly one element of type {kind.__name__}{marker} on the page:\n{self.current_page}'
            element = elements[0]
            element.value = text
            await self.trigger('keydown.enter', element=element)

    async def click(self, *,
                    kind: Type[T] = Element,
                    marker: Union[str, list[str], None] = None,
                    content: Union[str, list[str], None] = None,
                    ) -> None:
        """Perform a click event."""
        assert self.client
        with self.client:
            elements = await self.should_see(kind=kind, marker=marker, content=content)
            marker = f' with {marker=}' if marker is not None else ''
            content = f' with {content=}' if content is not None else ''
            assert len(elements) == 1, \
                f'expected to find exactly one element of type {kind.__name__}{marker}{content} on the page:\n{self.current_page}'
            element = elements[0]
            assert isinstance(element, ui.element)
            for listener in element._event_listeners.values():
                if listener.element_id != element.id:
                    continue
                args = None
                if isinstance(element, ui.checkbox):
                    args = not element.value
                events.handle_event(listener.handler,
                                    events.GenericEventArguments(sender=element, client=self.client, args=args))

    async def trigger(self, event: str, *,
                      kind: Type[T] = Element,
                      marker: Union[str, list[str], None] = None,
                      element: Optional[T] = None,
                      ) -> None:
        """Trigger the given event."""
        assert self.client
        with self.client:
            if element is None:
                elements = await self.should_see(kind=kind, marker=marker)
                element_type = kind.__name__
                marker = f' with {marker=}' if marker is not None else ''
                assert len(elements) == 1, \
                    f'expected to find exactly one element of type {element_type}{marker} on the page:\n{self.current_page}'
                element = elements[0]
            assert isinstance(element, ui.element)
            for listener in element._event_listeners.values():
                if listener.type != event:
                    continue
                events.handle_event(listener.handler,
                                    events.GenericEventArguments(sender=element, client=self.client, args={}))

    @property
    def current_page(self) -> Element:
        """Return the current page."""
        return self.client.layout


original_get_slot_stack = ng.Slot.get_stack
original_prune_slot_stack = ng.Slot.prune_stack


def get_stack(_=None) -> List[ng.Slot]:
    """Return the slot stack of the current client."""
    if User.current_user is None:
        return original_get_slot_stack()
    cls = ng.Slot
    client_id = id(User.current_user)
    if client_id not in cls.stacks:
        cls.stacks[client_id] = []
    return cls.stacks[client_id]


def prune_stack(cls) -> None:
    """Remove the current slot stack if it is empty."""
    if User.current_user is None:
        return original_prune_slot_stack()
    cls = ng.Slot
    client_id = id(User.current_user)
    if not cls.stacks[client_id]:
        del cls.stacks[client_id]


ng.Slot.get_stack = get_stack
ng.Slot.prune_stack = prune_stack
