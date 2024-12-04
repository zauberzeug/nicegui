from __future__ import annotations

import asyncio
import re
from typing import Any, List, Optional, Set, Type, TypeVar, Union, overload
from uuid import uuid4

import httpx
import socketio

from nicegui import Client, ElementFilter, ui
from nicegui.element import Element
from nicegui.nicegui import _on_handshake

from .user_download import UserDownload
from .user_interaction import UserInteraction
from .user_navigate import UserNavigate
from .user_notify import UserNotify

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
        self.navigate = UserNavigate(self)
        self.notify = UserNotify()
        self.download = UserDownload(self)

    @property
    def _client(self) -> Client:
        if self.client is None:
            raise ValueError('This user has not opened a page yet. Did you forgot to call .open()?')
        return self.client

    def __getattribute__(self, name: str) -> Any:
        if name not in {'notify', 'navigate', 'download'}:  # NOTE: avoid infinite recursion
            ui.navigate = self.navigate
            ui.notify = self.notify
            ui.download = self.download
        return super().__getattribute__(name)

    async def open(self, path: str, *, clear_forward_history: bool = True) -> Client:
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
        return self.client

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
                         marker: Union[str, List[str], None] = None,
                         content: Union[str, List[str], None] = None,
                         retries: int = 3,
                         ) -> None:
        ...

    async def should_see(self,
                         target: Union[str, Type[T], None] = None,
                         *,
                         kind: Optional[Type[T]] = None,
                         marker: Union[str, List[str], None] = None,
                         content: Union[str, List[str], None] = None,
                         retries: int = 3,
                         ) -> None:
        """Assert that the page contains an element fulfilling certain filter rules.

        Note that there is no scrolling in the user simulation -- the entire page is always *visible*.
        Due to asynchronous execution, sometimes the expected elements only appear after a short delay.

        By default `should_see` makes three attempts to find the element before failing.
        This can be adjusted with the `retries` parameter.
        """
        for _ in range(retries):
            with self._client:
                if self.notify.contains(target) or self._gather_elements(target, kind, marker, content):
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
                             marker: Union[str, List[str], None] = None,
                             content: Union[str, List[str], None] = None,
                             retries: int = 3,
                             ) -> None:
        ...

    async def should_not_see(self,
                             target: Union[str, Type[T], None] = None,
                             *,
                             kind: Optional[Type[T]] = None,
                             marker: Union[str, List[str], None] = None,
                             content: Union[str, List[str], None] = None,
                             retries: int = 3,
                             ) -> None:
        """Assert that the page does not contain an input with the given value."""
        for _ in range(retries):
            with self._client:
                if not self.notify.contains(target) and not self._gather_elements(target, kind, marker, content):
                    return
                await asyncio.sleep(0.05)
        raise AssertionError('expected not to see any ' + self._build_error_message(target, kind, marker, content))

    @overload
    def find(self,
             target: str,
             ) -> UserInteraction[Element]:
        ...

    @overload
    def find(self,
             target: Type[T],
             ) -> UserInteraction[T]:
        ...

    @overload
    def find(self: User,
             *,
             marker: Union[str, List[str], None] = None,
             content: Union[str, List[str], None] = None,
             ) -> UserInteraction[Element]:
        ...

    @overload
    def find(self,
             *,
             kind: Type[T],
             marker: Union[str, List[str], None] = None,
             content: Union[str, List[str], None] = None,
             ) -> UserInteraction[T]:
        ...

    def find(self,
             target: Union[str, Type[T], None] = None,
             *,
             kind: Optional[Type[T]] = None,
             marker: Union[str, List[str], None] = None,
             content: Union[str, List[str], None] = None,
             ) -> UserInteraction[T]:
        """Select elements for interaction."""
        with self._client:
            elements = self._gather_elements(target, kind, marker, content)
            if not elements:
                raise AssertionError('expected to find at least one ' +
                                     self._build_error_message(target, kind, marker, content))
        return UserInteraction(self, elements, target)

    @property
    def current_layout(self) -> Element:
        """Return the root layout element of the current page."""
        return self._client.layout

    def _gather_elements(
        self,
        target: Union[str, Type[T], None] = None,
        kind: Optional[Type[T]] = None,
        marker: Union[str, List[str], None] = None,
        content: Union[str, List[str], None] = None,
    ) -> Set[T]:
        if target is None:
            if kind is None:
                elements = set(ElementFilter(marker=marker, content=content))
            else:
                elements = set(ElementFilter(kind=kind, marker=marker, content=content))
        elif isinstance(target, str):
            elements = set(ElementFilter(marker=target)).union(ElementFilter(content=target))
        else:
            elements = set(ElementFilter(kind=target))
        return {e for e in elements if e.visible}  # type: ignore

    def _build_error_message(self,
                             target: Union[str, Type[T], None] = None,
                             kind: Optional[Type[T]] = None,
                             marker: Union[str, List[str], None] = None,
                             content: Union[str, List[str], None] = None,
                             ) -> str:
        if isinstance(target, str):
            return f'element with marker={target} or content={target} on the page:\n{self.current_layout}'
        elif target is not None:
            return f'element of type {target.__name__} on the page:\n{self.current_layout}'
        elif kind is not None:
            return f'element of type {kind.__name__} with {marker=} and {content=} on the page:\n{self.current_layout}'
        else:
            return f'element with {marker=} and {content=} on the page:\n{self.current_layout}'
