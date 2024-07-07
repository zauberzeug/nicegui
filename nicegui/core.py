from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING, Optional

from socketio import AsyncServer

if TYPE_CHECKING:
    from .air import Air
    from .app import App

app: App
sio: AsyncServer
loop: Optional[asyncio.AbstractEventLoop] = None
air: Optional[Air] = None
is_pytest: bool = 'PYTEST_CURRENT_TEST' in os.environ
