from __future__ import annotations

import asyncio
import inspect
import logging
import os
from contextlib import contextmanager
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, Iterator, List, Literal, Optional, Set, Union

from socketio import AsyncServer
from uvicorn import Server

from . import background_tasks

if TYPE_CHECKING:
    from .air import Air
    from .app import App
    from .client import Client
    from .language import Language
    from .slot import Slot


class State(Enum):
    STOPPED = 0
    STARTING = 1
    STARTED = 2
    STOPPING = 3


app: App
sio: AsyncServer
server: Server
loop: Optional[asyncio.AbstractEventLoop] = None
log: logging.Logger = logging.getLogger('nicegui')
state: State = State.STOPPED
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
air: Optional[Air] = None
storage_path: Path = Path(os.environ.get('NICEGUI_STORAGE_PATH', '.nicegui')).resolve()
socket_io_js_query_params: Dict = {}
socket_io_js_extra_headers: Dict = {}
socket_io_js_transports: List[Literal['websocket', 'polling']] = ['websocket', 'polling']  # NOTE: we favor websocket
_socket_id: Optional[str] = None
slot_stacks: Dict[int, List[Slot]] = {}
clients: Dict[str, Client] = {}
index_client: Client
quasar_config: Dict = {
    'brand': {
        'primary': '#5898d4',
    },
    'loadingBar': {
        'color': 'primary',
        'skipHijack': False,
    },
}

page_routes: Dict[Callable[..., Any], str] = {}

startup_handlers: List[Union[Callable[..., Any], Awaitable]] = []
shutdown_handlers: List[Union[Callable[..., Any], Awaitable]] = []
connect_handlers: List[Union[Callable[..., Any], Awaitable]] = []
disconnect_handlers: List[Union[Callable[..., Any], Awaitable]] = []
exception_handlers: List[Callable[..., Any]] = [log.exception]


def get_task_id() -> int:
    try:
        return id(asyncio.current_task())
    except RuntimeError:
        return 0


def get_slot_stack() -> List[Slot]:
    task_id = get_task_id()
    if task_id not in slot_stacks:
        slot_stacks[task_id] = []
    return slot_stacks[task_id]


def prune_slot_stack() -> None:
    task_id = get_task_id()
    if not slot_stacks[task_id]:
        del slot_stacks[task_id]


def get_slot() -> Slot:
    return get_slot_stack()[-1]


def get_client() -> Client:
    return get_slot().parent.client


@contextmanager
def socket_id(id_: str) -> Iterator[None]:
    global _socket_id  # pylint: disable=global-statement
    _socket_id = id_
    yield
    _socket_id = None


def handle_exception(exception: Exception) -> None:
    for handler in exception_handlers:
        result = handler() if not inspect.signature(handler).parameters else handler(exception)
        if isinstance(result, Awaitable):
            background_tasks.create(result)
