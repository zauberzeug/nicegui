import asyncio
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
        if self.shared:
            while self._shared_page is None:
                await asyncio.sleep(0.05)
            return self._shared_page
        else:
            page: Page = await self.function(request)
        return await page._route_function(request)

    def create_route(self, route: str) -> None:
        if self.shared:
            create_task(self.build())
        jp.Route(route, self.route_function)
