from __future__ import annotations

import asyncio
import re
from collections.abc import Callable, Iterator
from contextlib import AbstractContextManager, contextmanager
from typing import Any, TypeVar, overload
from uuid import uuid4

import httpx
import socketio

from nicegui import Client, ElementFilter, ui
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
        # Per-task stack of elements entered via `with user.scope(...):`. Keyed by asyncio task id
        # (like `Slot.stacks`) so a scope entered in one task never narrows lookups in another.
        # The innermost scope is the last element; an empty/absent stack means no active scope.
        self._scope_stack: dict[int, list[ui.element]] = {}
        self.javascript_rules: dict[re.Pattern, Callable[[re.Match], Any]] = {
            re.compile('.*__IS_DRAWER_OPEN__'): lambda _: True,  # see https://github.com/zauberzeug/nicegui/issues/4508
        }

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
        if name not in {'notify', 'navigate', 'download'}:  # avoid infinite recursion
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
        """
        for _ in range(retries):
            if self._sees(target, kind, marker, content):
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
        """Assert that the page does not contain an element fulfilling certain filter rules."""
        for _ in range(retries):
            if not self._sees(target, kind, marker, content):
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
        """Select elements for interaction."""
        elements = self._gather_elements(target, kind, marker, content)
        if not elements:
            raise AssertionError('expected to find at least one ' +
                                 self._build_error_message(target, kind, marker, content))
        return UserInteraction(self, elements, target)

    @overload
    def scope(self,
              target: str,
              ) -> AbstractContextManager[ui.element]:
        ...

    @overload
    def scope(self,
              target: type[T],
              ) -> AbstractContextManager[T]:
        ...

    @overload
    def scope(self,
              *,
              marker: str | list[str] | None = None,
              content: str | list[str] | None = None,
              ) -> AbstractContextManager[ui.element]:
        ...

    @overload
    def scope(self,
              *,
              kind: type[T],
              marker: str | list[str] | None = None,
              content: str | list[str] | None = None,
              ) -> AbstractContextManager[T]:
        ...

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
        markers or content in different parts of the layout.
        Inside the block, ``should_see``, ``should_not_see`` and ``find``
        only search the descendants of the entered element (the element itself is not matched)::

            with user.scope(marker='left-card'):
                await user.should_see('Button')  # only the button inside the left card
                await user.should_not_see('Other')

        The filter must match exactly one element; otherwise an ``AssertionError`` is raised,
        because scoping to an ambiguous match would hide the very bugs this feature helps catch.
        The element must already exist:
        entering a scope does not retry like ``should_see``,
        so wait for asynchronously created content with ``await user.should_see(...)`` first.

        The scope only applies to the task that entered it:
        assertions running in a task created inside the block, e.g. by ``asyncio.gather``,
        still search the whole page.
        """
        elements = self._gather_elements(target, kind, marker, content)
        if len(elements) != 1:
            raise AssertionError(f'expected exactly one element to scope to, but found {len(elements)}: ' +
                                 self._build_error_message(target, kind, marker, content))
        (element,) = elements
        task_id = get_task_id()
        stack = self._scope_stack.setdefault(task_id, [])
        stack.append(element)
        try:
            with element:
                yield element
        finally:
            stack.pop()
            if not stack:
                del self._scope_stack[task_id]

    @property
    def current_layout(self) -> ui.element:
        """Return the root layout element of the current page."""
        return self._client.layout

    def _current_scope(self) -> ui.element | None:
        """Return the innermost element entered via ``scope()`` in the current task, if any."""
        stack = self._scope_stack.get(get_task_id())
        if not stack:
            return None
        scope = stack[-1]
        if scope.is_deleted:
            # Without this check every lookup would silently find nothing, because a deleted element
            # is no longer an ancestor of anything -- making `should_not_see` pass for the wrong reason.
            raise AssertionError('expected the element entered via `user.scope(...)` to still exist, but '
                                 f'{str(scope).splitlines()[0]} has been deleted, e.g. by refreshing or clearing '
                                 'its container; enter the scope again after rebuilding it')
        return scope

    def _sees(
        self,
        target: str | type[T] | None = None,
        kind: type[T] | None = None,
        marker: str | list[str] | None = None,
        content: str | list[str] | None = None,
    ) -> bool:
        """Return whether an element or notification matching the given filter is currently visible."""
        if self._current_scope() is None and self.notify.contains(target):
            return True  # notifications are page-level, so a scoped search must not match them
        return bool(self._gather_elements(target, kind, marker, content))

    def _gather_elements(
        self,
        target: str | type[T] | None = None,
        kind: type[T] | None = None,
        marker: str | list[str] | None = None,
        content: str | list[str] | None = None,
    ) -> set[T]:
        scope = self._current_scope()

        def make_filter(**kwargs: Any) -> ElementFilter[Any]:
            # `local_scope=False` covers the whole layout (header, drawer, footer, notifications),
            # independent of the ambient slot stack and of `ElementFilter.DEFAULT_LOCAL_SCOPE`.
            # Inside a `with user.scope(...):` block, only descendants of the innermost entered element remain.
            element_filter = ElementFilter(only_visible=True, local_scope=False, **kwargs)
            return element_filter.within(instance=scope) if scope is not None else element_filter

        with self._client:
            if target is None:
                elements = set(make_filter(kind=kind, marker=marker, content=content))
            elif isinstance(target, str):
                elements = set(make_filter(marker=target)).union(make_filter(content=target))
            else:
                elements = set(make_filter(kind=target))
        return elements  # type: ignore

    def _build_error_message(self,
                             target: str | type[T] | None = None,
                             kind: type[T] | None = None,
                             marker: str | list[str] | None = None,
                             content: str | list[str] | None = None,
                             ) -> str:
        if isinstance(target, str):
            description = f'element with marker={target} or content={target}'
        elif target is not None:
            description = f'element of type {target.__name__}'
        elif kind is not None:
            description = f'element of type {kind.__name__} with {marker=} and {content=}'
        else:
            description = f'element with {marker=} and {content=}'
        scope = self._current_scope()
        if scope is None:
            return f'{description} on the page:\n{self.current_layout}'
        # The first line of an element's string representation describes the element itself,
        # the remaining lines its subtree -- which is exactly what the search covered.
        tree = str(scope)
        return f'{description} within {tree.splitlines()[0]}:\n{tree}'
