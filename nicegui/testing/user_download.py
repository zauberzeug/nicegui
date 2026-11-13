from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING

import httpx2

from .. import background_tasks

if TYPE_CHECKING:
    from .user import User


class UserDownload:

    def __init__(self, user: User) -> None:
        self.http_responses: list[httpx2.Response] = []
        self.user = user

    def _start(self, src: str | bytes) -> None:
        background_tasks.create(self._get(src),
                                name=f'download {str(src[:10]) + "..." if isinstance(src, bytes) else src}')

    async def _get(self, src: str | bytes) -> None:
        if isinstance(src, bytes):
            await asyncio.sleep(0)
            response = httpx2.Response(httpx2.codes.OK, content=src)
        else:
            response = await self.user.http_client.get(src)
        self.http_responses.append(response)

    async def next(self, *, timeout: float = 1.0) -> httpx2.Response:
        """Wait for a new download to happen.

        :param timeout: the maximum time to wait (default: 1.0)
        :returns: the HTTP response
        """
        assert self.user.client
        downloads = len(self.http_responses)
        deadline = time.time() + timeout
        while len(self.http_responses) < downloads + 1:
            await asyncio.sleep(0.1)
            if time.time() > deadline:
                raise TimeoutError('Download did not happen')
        return self.http_responses[-1]
