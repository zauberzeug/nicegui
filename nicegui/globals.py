from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Literal, Optional, Union

from socketio import AsyncServer
from uvicorn import Server

if TYPE_CHECKING:
    from .app import App
    from .language import Language

app: App
sio: AsyncServer
server: Server
loop: Optional[asyncio.AbstractEventLoop] = None
ui_run_has_been_called: bool = False

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
socket_io_js_query_params: Dict = {}
socket_io_js_extra_headers: Dict = {}
socket_io_js_transports: List[Literal['websocket', 'polling']] = ['websocket', 'polling']  # NOTE: we favor websocket
quasar_config: Dict = {
    'brand': {
        'primary': '#5898d4',
    },
    'loadingBar': {
        'color': 'primary',
        'skipHijack': False,
    },
}
