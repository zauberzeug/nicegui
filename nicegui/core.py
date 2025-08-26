from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Callable

from socketio import AsyncServer

if TYPE_CHECKING:
    from .air import Air
    from .app import App

app: App
sio: AsyncServer
loop: asyncio.AbstractEventLoop | None = None
air: Air | None = None
spa: Callable | None = None
