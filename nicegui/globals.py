from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Literal, Optional, Set, Union

from socketio import AsyncServer
from uvicorn import Server

if TYPE_CHECKING:
    from .app import App
    from .client import Client
    from .language import Language
    from .slot import Slot

app: App
sio: AsyncServer
server: Server
loop: Optional[asyncio.AbstractEventLoop] = None
ui_run_has_been_called: bool = False
optional_features: Set[str] = set()

reload: bool
title: str
viewport: str
favicon: Optional[Union[str, Path]]
dark: Optional[bool]
language: Language
binding_refresh_interval: float
reconnect_timeout: float
tailwind: bool
prod_js: bool
endpoint_documentation: Literal['none', 'internal', 'page', 'all'] = 'none'
storage_path: Path = Path(os.environ.get('NICEGUI_STORAGE_PATH', '.nicegui')).resolve()
socket_io_js_query_params: Dict = {}
socket_io_js_extra_headers: Dict = {}
socket_io_js_transports: List[Literal['websocket', 'polling']] = ['websocket', 'polling']  # NOTE: we favor websocket
slot_stacks: Dict[int, List[Slot]] = {}
quasar_config: Dict = {
    'brand': {
        'primary': '#5898d4',
    },
    'loadingBar': {
        'color': 'primary',
        'skipHijack': False,
    },
}


def get_task_id() -> int:
    """Return the ID of the current asyncio task."""
    try:
        return id(asyncio.current_task())
    except RuntimeError:
        return 0


def get_slot_stack() -> List[Slot]:
    """Return the slot stack of the current asyncio task."""
    task_id = get_task_id()
    if task_id not in slot_stacks:
        slot_stacks[task_id] = []
    return slot_stacks[task_id]


def prune_slot_stack() -> None:
    """Remove the current slot stack if it is empty."""
    task_id = get_task_id()
    if not slot_stacks[task_id]:
        del slot_stacks[task_id]


def get_slot() -> Slot:
    """Return the current slot."""
    return get_slot_stack()[-1]


def get_client() -> Client:
    """Return the current client."""
    return get_slot().parent.client
