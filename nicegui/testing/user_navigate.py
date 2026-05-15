from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

from nicegui import Client, background_tasks, ui
from nicegui.elements.sub_pages import SubPages
from nicegui.functions.navigate import Navigate
from nicegui.sub_pages_router import has_any_unresolved_path

if TYPE_CHECKING:
    from .user import User


class UserNavigate(Navigate):

    def __init__(self, user: User) -> None:
        super().__init__()
        self.user = user

    def to(self, target: Callable[..., Any] | str | ui.element, new_tab: bool = False) -> None:
        if isinstance(target, ui.element):
            # NOTE navigation to an element does not do anything in the user simulation (the whole content is always visible)
            return
        path = Client.page_routes[target] if callable(target) else target
        background_tasks.create(self._open(path, clear_forward_history=True), name=f'navigate to {path}')

    def back(self) -> None:
        current = self.user.back_history.pop()
        self.user.forward_history.append(current)
        target = self.user.back_history.pop()
        background_tasks.create(self._open(target, clear_forward_history=False), name=f'navigate back to {target}')

    def forward(self) -> None:
        if not self.user.forward_history:
            return
        target = self.user.forward_history[0]
        del self.user.forward_history[0]
        background_tasks.create(self._open(target, clear_forward_history=False), name=f'navigate forward to {target}')

    def reload(self) -> None:
        target = self.user.back_history.pop()
        background_tasks.create(self.user.open(target, clear_forward_history=False),
                                name=f'navigate reload to {target}')

    async def _open(self, path: str, *, clear_forward_history: bool) -> None:
        client = self.user.client
        parsed_url = urlparse(path)
        if (
            client is None or  # user is not yet on any page
            parsed_url.scheme or parsed_url.netloc or  # path is absolute URL
            not any(isinstance(el, SubPages) for el in client.layout.descendants())  # no SubPages in the layout
        ):
            await self.user.open(path, clear_forward_history=clear_forward_history)  # full page reload
            return

        router = client.sub_pages_router
        with client:
            await router._handle_open(path)  # pylint: disable=protected-access
        if has_any_unresolved_path(client) and router._other_page_builder_matches_path(path, client):  # pylint: disable=protected-access
            await self.user.open(path, clear_forward_history=clear_forward_history)  # fallback to full page reload
            return

        self.user.back_history.append(path)
        if clear_forward_history:
            self.user.forward_history.clear()
