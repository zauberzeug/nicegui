from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from nicegui import Client, background_tasks
from nicegui.element import Element
from nicegui.elements.sub_pages import SubPages
from nicegui.functions.navigate import Navigate

if TYPE_CHECKING:
    from .user import User


class UserNavigate(Navigate):

    def __init__(self, user: User) -> None:
        super().__init__()
        self.user = user

    def to(self, target: Callable[..., Any] | str | Element, new_tab: bool = False) -> None:
        if isinstance(target, Element):
            # NOTE navigation to an element does not do anything in the user simulation (the whole content is always visible)
            return
        path = Client.page_routes[target] if callable(target) else target
        background_tasks.create(self.user.open(path), name=f'navigate to {path}')

    def back(self) -> None:
        current = self.user.back_history.pop()
        self.user.forward_history.append(current)
        target = self.user.back_history.pop()
        background_tasks.create(self._navigate_to(target, clear_forward_history=False),
                                name=f'navigate back to {target}')

    def forward(self) -> None:
        if not self.user.forward_history:
            return
        target = self.user.forward_history[0]
        del self.user.forward_history[0]
        background_tasks.create(self._navigate_to(target, clear_forward_history=False),
                                name=f'navigate forward to {target}')

    async def _navigate_to(self, path: str, clear_forward_history: bool = True) -> None:
        if self.user.client:
            sub_pages_elements = [el for el in self.user.client.layout.descendants() if isinstance(el, SubPages)]
            if sub_pages_elements:
                with self.user.client:
                    await self.user.client.sub_pages_router._handle_open(path)  # pylint: disable=protected-access
                if clear_forward_history:
                    self.user.forward_history.clear()
                self.user.back_history.append(path)
                return
        await self.user.open(path, clear_forward_history=clear_forward_history)

    def reload(self) -> None:
        target = self.user.back_history.pop()
        background_tasks.create(self.user.open(target, clear_forward_history=False),
                                name=f'navigate reload to {target}')
