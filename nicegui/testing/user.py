from __future__ import annotations

import asyncio
import re
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any, TypeVar, overload
from uuid import uuid4

import httpx
import socketio

from nicegui import Client, ElementFilter, context, ui
from nicegui.nicegui import _on_handshake
from nicegui.outbox import Message
from nicegui.slot import get_task_id

from .user_download import UserDownload
from .user_interaction import UserInteraction
from .user_navigate import UserNavigate
from .user_notify import UserNotify

# pylint: disable=protected-access


T = TypeVar('T', bound=ui.element)


class User:
    current_user: User | None = None

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.http_client = client
        self.sio = socketio.AsyncClient()
        self.client: Client | None = None
        self.back_history: list[str] = []
        self.forward_history: list[str] = []
        self.navigate = UserNavigate(self)
        self.notify = UserNotify()
        self.download = UserDownload(self)
        self.tab_id = str(uuid4())
        # Per-task nesting depth of active `with user.scope(...):` blocks. Keyed by asyncio task id
        # (like `Slot.stacks`) so a scope entered in one task never narrows lookups in another.
        self._scope_depth: dict[int, int] = {}
        self.javascript_rules: dict[re.Pattern, Callable[[re.Match], Any]] = {
            re.compile('.*__IS_DRAWER_OPEN__'): lambda _: True,  # see https://github.com/zauberzeug/nicegui/issues/4508
        }

    @property
    def _scope(self) -> ui.element | Client:
        if not context.slot_stack:
            return self._client
        if context.client is not self._client:
            # fall back to the bound client if the slot stack belongs to a different page
            return self._client
        if context.slot.parent is context.client.content:
            # fall back to the bound client's layout when the current slot is the page content for backward compatibility
            return self._client
        return context.slot.parent

    @property
    def _client(self) -> Client:
        if self.client is None:
            raise ValueError('This user has not opened a page yet. Did you forgot to call .open()?')
        return self.client

    def __enter__(self) -> Client:
        return self._client.__enter__()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        return self._client.__exit__(exc_type, exc_val, exc_tb)

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
        await _on_handshake(f'test-{uuid4()}', {
            'client_id': self.client.id,
            'tab_id': self.tab_id,
            'document_id': str(uuid4()),
        })
        self.back_history.append(path)
        if clear_forward_history:
            self.forward_history.clear()
        self._patch_outbox_emit_function()
        return self.client

    def _patch_outbox_emit_function(self) -> None:
        original_emit = self._client.outbox._emit

        async def simulated_emit(message: Message) -> None:
            await original_emit(message)
            _, type_, data = message
            if type_ == 'run_javascript':
                for rule, result in self.javascript_rules.items():
                    match = rule.match(data['code'])
                    if match:
                        self._client.handle_javascript_response({
                            'request_id': data['request_id'],
                            'result': result(match),
                        })

        self._client.outbox._emit = simulated_emit  # type: ignore

    @overload
    async def should_see(self,
                         target: str | type[T],
                         *,
                         retries: int = 3,
                         ) -> None:
        ...

    @overload
    async def should_see(self,
                         *,
                         kind: type[T] | None = None,
                         marker: str | list[str] | None = None,
                         content: str | list[str] | None = None,
                         retries: int = 3,
                         ) -> None:
        ...

    async def should_see(self,
                         target: str | type[T] | None = None,
                         *,
                         kind: type[T] | None = None,
                         marker: str | list[str] | None = None,
                         content: str | list[str] | None = None,
                         retries: int = 3,
                         ) -> None:
        """Assert that the page contains an element fulfilling certain filter rules.

        Note that there is no scrolling in the user simulation -- the entire page is always *visible*.
        Due to asynchronous execution, sometimes the expected elements only appear after a short delay.

        By default `should_see` makes three attempts to find the element before failing.
        This can be adjusted with the `retries` parameter.

        To limit the search to one part of a page that reuses markers or content, wrap the
        assertion in a ``with user.scope(...):`` block (see ``User.scope``).
        """
        for _ in range(retries):
            if self.notify.contains(target) or self._gather_elements(target=target, kind=kind, marker=marker, content=content):
                return
            await asyncio.sleep(0.1)
        raise AssertionError('expected to see at least one ' + self._build_error_message(target, kind, marker, content))

    @overload
    async def should_not_see(self,
                             target: str | type[T],
                             *,
                             retries: int = 3,
                             ) -> None:
        ...

    @overload
    async def should_not_see(self,
                             *,
                             kind: type[T] | None = None,
                             marker: str | list[str] | None = None,
                             content: str | list[str] | None = None,
                             retries: int = 3,
                             ) -> None:
        ...

    async def should_not_see(self,
                             target: str | type[T] | None = None,
                             *,
                             kind: type[T] | None = None,
                             marker: str | list[str] | None = None,
                             content: str | list[str] | None = None,
                             retries: int = 3,
                             ) -> None:
        """Assert that the page does not contain an element fulfilling certain filter rules.

        To limit the search to one part of a page that reuses markers or content, wrap the
        assertion in a ``with user.scope(...):`` block (see ``User.scope``).
        """
        for _ in range(retries):
            if not self.notify.contains(target) and not self._gather_elements(target=target, kind=kind, marker=marker, content=content):
                return
            await asyncio.sleep(0.05)
        raise AssertionError('expected not to see any ' + self._build_error_message(target, kind, marker, content))

    @overload
    def find(self,
             target: str,
             ) -> UserInteraction[ui.element]:
        ...

    @overload
    def find(self,
             target: type[T],
             ) -> UserInteraction[T]:
        ...

    @overload
    def find(self: User,
             *,
             marker: str | list[str] | None = None,
             content: str | list[str] | None = None,
             ) -> UserInteraction[ui.element]:
        ...

    @overload
    def find(self,
             *,
             kind: type[T],
             marker: str | list[str] | None = None,
             content: str | list[str] | None = None,
             ) -> UserInteraction[T]:
        ...

    def find(self,
             target: str | type[T] | None = None,
             *,
             kind: type[T] | None = None,
             marker: str | list[str] | None = None,
             content: str | list[str] | None = None,
             ) -> UserInteraction[T]:
        """Select elements for interaction.

        To limit the search to one part of a page that reuses markers or content, wrap the
        call in a ``with user.scope(...):`` block (see ``User.scope``).
        """
        elements = self._gather_elements(target=target, kind=kind, marker=marker, content=content)
        if not elements:
            raise AssertionError('expected to find at least one ' +
                                 self._build_error_message(target, kind, marker, content))
        return UserInteraction(self, elements, target)

    @contextmanager
    def scope(self,
              target: str | type[T] | None = None,
              *,
              kind: type[T] | None = None,
              marker: str | list[str] | None = None,
              content: str | list[str] | None = None,
              ) -> Iterator[T]:
        """Enter the single element matching the given filter, scoping all lookups inside the block to it.

        This is the recommended way to write assertions against pages that intentionally reuse
        markers or content in different parts of the layout. Inside the block, ``should_see``,
        ``should_not_see`` and ``find`` only search within the entered element::

            with user.scope(marker='left-card'):
                await user.should_see('Button')  # only the button inside the left card
                await user.should_not_see('Other')

        The filter must match exactly one element; otherwise an ``AssertionError`` is raised,
        because scoping to an ambiguous match would hide the very bugs this feature helps catch.
        """
        elements = self._gather_elements(target=target, kind=kind, marker=marker, content=content)
        if len(elements) != 1:
            raise AssertionError(f'expected exactly one element to scope to, but found {len(elements)}: ' +
                                 self._build_error_message(target, kind, marker, content))
        (element,) = elements
        task_id = get_task_id()
        self._scope_depth[task_id] = self._scope_depth.get(task_id, 0) + 1
        try:
            with element:
                yield element
        finally:
            if self._scope_depth[task_id] > 1:
                self._scope_depth[task_id] -= 1
            else:
                del self._scope_depth[task_id]

    @property
    def current_layout(self) -> ui.element:
        """Return the root layout element of the current page."""
        return self._client.layout

    def _gather_elements(
        self,
        *,
        target: str | type[T] | None = None,
        kind: type[T] | None = None,
        marker: str | list[str] | None = None,
        content: str | list[str] | None = None,
    ) -> set[T]:
        scope = self._scope
        # Narrow the search only while the current task is inside a `with user.scope(...):` block,
        # where the scope resolves to a real sub-element. The `not isinstance(scope, Client)` guard
        # is a safety net so that page-level lookups never narrow to the client content root, which
        # would drop the layout shells (header, drawer, footer, notifications).
        local_scope = self._scope_depth.get(get_task_id(), 0) > 0 and not isinstance(scope, Client)
        with scope:
            if target is None:
                if kind is None:
                    elements = set(ElementFilter(marker=marker, content=content,
                                                 only_visible=True, local_scope=local_scope))
                else:
                    elements = set(ElementFilter(kind=kind, marker=marker,
                                                 content=content, only_visible=True, local_scope=local_scope))
            elif isinstance(target, str):
                elements = set(ElementFilter(marker=target, only_visible=True, local_scope=local_scope)) \
                    .union(ElementFilter(content=target, only_visible=True, local_scope=local_scope))
            else:
                elements = set(ElementFilter(kind=target, only_visible=True, local_scope=local_scope))
        return elements  # type: ignore

    def _build_error_message(self,
                             target: str | type[T] | None = None,
                             kind: type[T] | None = None,
                             marker: str | list[str] | None = None,
                             content: str | list[str] | None = None,
                             ) -> str:
        if isinstance(target, str):
            return f'element with marker={target} or content={target} on the page:\n{self.current_layout}'
        elif target is not None:
            return f'element of type {target.__name__} on the page:\n{self.current_layout}'
        elif kind is not None:
            return f'element of type {kind.__name__} with {marker=} and {content=} on the page:\n{self.current_layout}'
        else:
            return f'element with {marker=} and {content=} on the page:\n{self.current_layout}'
