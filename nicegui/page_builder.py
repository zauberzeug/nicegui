from dataclasses import dataclass
from typing import TYPE_CHECKING, Awaitable, Callable, Optional

import justpy as jp
from starlette.requests import Request

from .task_logger import create_task

if TYPE_CHECKING:
    from .page import Page


@dataclass
class PageBuilder:
    function: Callable[[], Awaitable['Page']]
    shared: bool

    _shared_page: Optional['Page'] = None

    async def build(self) -> None:
        assert self.shared
        self._shared_page = await self.function()

    async def route_function(self, request: Request) -> 'Page':
        page = self._shared_page if self.shared else await self.function()
        return await page._route_function(request)

    def create_route(self, route: str) -> None:
        if self.shared:
            create_task(self.build())
        jp.Route(route, self.route_function)
