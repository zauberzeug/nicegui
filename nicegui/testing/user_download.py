from __future__ import annotations

import asyncio
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any

import httpx

from .. import background_tasks
from ..functions.download import Download

if TYPE_CHECKING:
    from .user import User


class UserDownload(Download):

    def __init__(self, user: User) -> None:
        self.http_responses: list[httpx.Response] = []
        self.user = user

    def __call__(self, src: str | Path | bytes, filename: str | None = None, media_type: str = '') -> Any:
        background_tasks.create(self._get(src),
                                name=f'download {str(src[:10]) + "..." if isinstance(src, bytes) else src}')

    def file(self, path: str | Path, filename: str | None = None, media_type: str = '') -> None:
        self(path)

    def from_url(self, url: str, filename: str | None = None, media_type: str = '') -> None:
        self(url)

    def content(self, content: bytes | str, filename: str | None = None, media_type: str = '') -> None:
        self(content)

    async def _get(self,  src: str | Path | bytes) -> None:
        if isinstance(src, bytes):
            await asyncio.sleep(0)
            response = httpx.Response(httpx.codes.OK, content=src)
        else:
            response = await self.user.http_client.get(str(src))
        self.http_responses.append(response)

    async def next(self, *, timeout: float = 1.0) -> httpx.Response:
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
