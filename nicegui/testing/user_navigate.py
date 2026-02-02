from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from nicegui import Client, background_tasks
from nicegui.element import Element
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
        background_tasks.create(self.user.open(target, clear_forward_history=False), name=f'navigate back to {target}')

    def forward(self) -> None:
        if not self.user.forward_history:
            return
        target = self.user.forward_history[0]
        del self.user.forward_history[0]
        background_tasks.create(self.user.open(target, clear_forward_history=False),
                                name=f'navigate forward to {target}')

    def reload(self) -> None:
        target = self.user.back_history.pop()
        background_tasks.create(self.user.open(target, clear_forward_history=False),
                                name=f'navigate reload to {target}')
