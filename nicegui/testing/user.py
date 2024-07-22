from __future__ import annotations

import asyncio
import re
from typing import Any, Callable, List, Optional, Set, Type, TypeVar, Union, overload
from uuid import uuid4

import httpx
import socketio
from typing_extensions import Self

from nicegui import Client, ElementFilter, background_tasks, ui
from nicegui.element import Element
from nicegui.functions.navigate import Navigate
from nicegui.nicegui import Slot, _on_handshake

from .user_interaction import UserInteraction

# pylint: disable=protected-access


T = TypeVar('T', bound=Element)


class User:
    current_user: Optional[User] = None

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.http_client = client
        self.sio = socketio.AsyncClient()
        self.client: Optional[Client] = None
        self.back_history: List[str] = []
        self.forward_history: List[str] = []

    async def open(self, path: str, clear_forward_history=True) -> None:
        """Open the given path."""
        response = await self.http_client.get(path, follow_redirects=True)
        assert response.status_code == 200, f'Expected status code 200, got {response.status_code}'
        if response.headers.get('X-Nicegui-Content') != 'page':
            raise ValueError(f'Expected a page response, got {response.text}')

        match = re.search(r"'client_id': '([0-9a-f-]+)'", response.text)
        assert match is not None
        client_id = match.group(1)
        self.client = Client.instances[client_id]
        self.sio.on('connect')
        await _on_handshake(f'test-{uuid4()}', {'client_id': self.client.id, 'tab_id': str(uuid4())})
        self.back_history.append(path)
        if clear_forward_history:
            self.forward_history.clear()
        self.activate()

    def activate(self) -> Self:
        """Activate the user for interaction."""
        if self.current_user:
            self.current_user.deactivate()
        self.current_user = self
        assert self.client
        ui.navigate = UserNavigate(self)
        self.client.__enter__()
        return self

    def deactivate(self, *_) -> None:
        """Deactivate the user."""
        assert self.client
        self.client.__exit__()
        self.current_user = None

    @overload
    async def should_see(self,
                         target: Union[str, Type[T]],
                         *,
                         retries: int = 3,
                         ) -> None:
        ...

    @overload
    async def should_see(self,
                         *,
                         kind: Optional[Type[T]] = None,
                         marker: Union[str, list[str], None] = None,
                         content: Union[str, list[str], None] = None,
                         retries: int = 3,
                         ) -> None:
        ...

    async def should_see(self,
                         target: Union[str, Type[T], None] = None,
                         *,
                         kind: Optional[Type[T]] = None,
                         marker: Union[str, list[str], None] = None,
                         content: Union[str, list[str], None] = None,
                         retries: int = 3,
                         ) -> None:
        """Assert that the page contains an input with the given value."""
        assert self.client
        for _ in range(retries):
            with self.client:
                if self._gather_elements(target, kind, marker, content):
                    return
                await asyncio.sleep(0.1)
        raise AssertionError('expected to see at least one ' + self._build_error_message(target, kind, marker, content))

    @overload
    async def should_not_see(self,
                             target: Union[str, Type[T]],
                             *,
                             retries: int = 3,
                             ) -> None:
        ...

    @overload
    async def should_not_see(self,
                             *,
                             kind: Optional[Type[T]] = None,
                             marker: Union[str, list[str], None] = None,
                             content: Union[str, list[str], None] = None,
                             retries: int = 3,
                             ) -> None:
        ...

    async def should_not_see(self,
                             target: Union[str, Type[T], None] = None,
                             *,
                             kind: Optional[Type[T]] = None,
                             marker: Union[str, list[str], None] = None,
                             content: Union[str, list[str], None] = None,
                             retries: int = 3,
                             ) -> None:
        """Assert that the page does not contain an input with the given value."""
        assert self.client
        for _ in range(retries):
            with self.client:
                if not self._gather_elements(target, kind, marker, content):
                    return
                await asyncio.sleep(0.05)
        raise AssertionError('expected not to see any ' + self._build_error_message(target, kind, marker, content))

    @overload
    def find(self,
             target: Union[str, Type[T]],
             ) -> UserInteraction:
        ...

    @overload
    def find(self,
             *,
             kind: Type[T] = Element,
             marker: Union[str, list[str], None] = None,
             content: Union[str, list[str], None] = None,
             ) -> UserInteraction:
        ...

    def find(self,
             target: Union[str, Type[T], None] = None,
             *,
             kind: Optional[Type[T]] = None,
             marker: Union[str, list[str], None] = None,
             content: Union[str, list[str], None] = None,
             ) -> UserInteraction:
        """Select elements for interaction."""
        assert self.client
        with self.client:
            elements = self._gather_elements(target, kind, marker, content)
            if not elements:
                raise AssertionError('expected to find at least one ' +
                                     self._build_error_message(target, kind, marker, content))
        return UserInteraction(self, elements)

    @property
    def current_layout(self) -> Element:
        """Return the root layout element of the current page."""
        assert self.client
        return self.client.layout

    def _gather_elements(self,
                         target: Union[str, Type[T], None] = None,
                         kind: Optional[Type[T]] = None,
                         marker: Union[str, list[str], None] = None,
                         content: Union[str, list[str], None] = None,
                         ) -> Set[T]:
        if target is None:
            return set(ElementFilter(kind=kind, marker=marker, content=content))
        elif isinstance(target, str):
            return set(ElementFilter(marker=target)).union(ElementFilter(content=target))
        else:
            return set(ElementFilter(kind=target))

    def _build_error_message(self,
                             target: Union[str, Type[T], None] = None,
                             kind: Optional[Type[T]] = None,
                             marker: Union[str, list[str], None] = None,
                             content: Union[str, list[str], None] = None,
                             ) -> str:
        if isinstance(target, str):
            return f'element with marker={target} or content={target} on the page:\n{self.current_layout}'
        elif target is not None:
            return f'element of type {target.__name__} on the page:\n{self.current_layout}'
        elif kind is not None:
            return f'element of type {kind.__name__} with {marker=} and {content=} on the page:\n{self.current_layout}'
        else:
            return f'element with {marker=} and {content=} on the page:\n{self.current_layout}'


original_get_slot_stack = Slot.get_stack
original_prune_slot_stack = Slot.prune_stack


def get_stack(_=None) -> List[Slot]:
    """Return the slot stack of the current client."""
    if User.current_user is None:
        return original_get_slot_stack()
    cls = Slot
    client_id = id(User.current_user)
    if client_id not in cls.stacks:
        cls.stacks[client_id] = []
    return cls.stacks[client_id]


def prune_stack(cls) -> None:
    """Remove the current slot stack if it is empty."""
    if User.current_user is None:
        original_prune_slot_stack()
        return
    cls = Slot
    client_id = id(User.current_user)
    if not cls.stacks[client_id]:
        del cls.stacks[client_id]


Slot.get_stack = get_stack  # type: ignore
Slot.prune_stack = prune_stack  # type: ignore


class UserNavigate(Navigate):
    def __init__(self, user: User) -> None:
        self.user = user

    def to(self, target: Union[Callable[..., Any], str, Element], new_tab: bool = False) -> None:
        if isinstance(target, Element):
            # NOTE navigation to an element does not do anything in the user simulation (the whole content is always visible)
            return
        path = Client.page_routes[target] if callable(target) else target
        background_tasks.create(self.user.open(path))

    def back(self) -> None:
        current = self.user.back_history.pop()
        self.user.forward_history.append(current)
        target = self.user.back_history.pop()
        background_tasks.create(self.user.open(target, clear_forward_history=False))

    def forward(self) -> None:
        if not self.user.forward_history:
            return
        target = self.user.forward_history[0]
        del self.user.forward_history[0]
        background_tasks.create(self.user.open(target, clear_forward_history=False))
