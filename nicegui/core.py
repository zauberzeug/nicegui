from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import TYPE_CHECKING

from socketio import AsyncServer

if TYPE_CHECKING:
    from .air import Air
    from .app import App
    from .client import Client

app: App
sio: AsyncServer
loop: asyncio.AbstractEventLoop | None = None
air: Air | None = None
root: Callable | None = None
script_mode: bool = False
script_client: Client | None = None


def is_script_mode_preflight() -> bool:
    """Return whether this is the preflight run of the script mode."""
    return script_mode and not app.is_started  # pylint: disable=undefined-variable # noqa: F821


def reset() -> None:
    """Reset core variables. (Useful for testing.)"""
    global loop, air, root, script_mode, script_client  # pylint: disable=global-statement # noqa: PLW0603
    loop = None
    air = None
    root = None
    script_mode = False
    script_client = None
