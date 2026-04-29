from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

from nicegui import Client, background_tasks, ui
from nicegui.elements.sub_pages import SubPages
from nicegui.functions.navigate import Navigate

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
        background_tasks.create(self._open(path), name=f'navigate to {path}')

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
        background_tasks.create(self._open(target, clear_forward_history=False), name=f'navigate reload to {target}')

    async def _open(self, path: str, *, clear_forward_history: bool = True) -> None:
        if self.user.client is not None:
            parsed = urlparse(path)
            if not parsed.scheme and not parsed.netloc and \
                    any(isinstance(el, SubPages) for el in self.user.client.layout.descendants()):
                with self.user.client:
                    await self.user.client.sub_pages_router._handle_open(path)  # pylint: disable=protected-access
                self.user.back_history.append(path)
                if clear_forward_history:
                    self.user.forward_history.clear()
                return
        await self.user.open(path, clear_forward_history=clear_forward_history)
