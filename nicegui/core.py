from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Optional

from socketio import AsyncServer

if TYPE_CHECKING:
    from .air import Air
    from .app import App

app: App
sio: AsyncServer
loop: Optional[asyncio.AbstractEventLoop] = None
air: Optional[Air] = None
