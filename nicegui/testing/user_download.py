from __future__ import annotations

import asyncio
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any, List, Optional, Union

import httpx

from .. import background_tasks

if TYPE_CHECKING:
    from .user import User


class UserDownload:

    def __init__(self, user: User) -> None:
        self.http_responses: List[httpx.Response] = []
        self.user = user

    def __call__(self, src: Union[str, Path, bytes], filename: Optional[str] = None, media_type: str = '') -> Any:
        background_tasks.create(self._get(src))

    async def _get(self,  src: Union[str, Path, bytes]) -> None:
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
