import asyncio
import inspect
import logging
from contextlib import contextmanager
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, Iterator, List, Optional, Union

from socketio import AsyncServer
from uvicorn import Server

from . import background_tasks
from .app import App
from .language import Language

if TYPE_CHECKING:
    from .air import Air
    from .client import Client
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
optional_features: List[str] = []

reload: bool
title: str
viewport: str
favicon: Optional[Union[str, Path]]
dark: Optional[bool]
language: Language
binding_refresh_interval: float
tailwind: bool
air: Optional['Air'] = None
socket_io_js_extra_headers: Dict = {}

_socket_id: Optional[str] = None
slot_stacks: Dict[int, List['Slot']] = {}
clients: Dict[str, 'Client'] = {}
index_client: 'Client'

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


def get_slot_stack() -> List['Slot']:
    task_id = get_task_id()
    if task_id not in slot_stacks:
        slot_stacks[task_id] = []
    return slot_stacks[task_id]


def prune_slot_stack() -> None:
    task_id = get_task_id()
    if not slot_stacks[task_id]:
        del slot_stacks[task_id]


def get_slot() -> 'Slot':
    return get_slot_stack()[-1]


def get_client() -> 'Client':
    return get_slot().parent.client


@contextmanager
def socket_id(id: str) -> Iterator[None]:
    global _socket_id
    _socket_id = id
    yield
    _socket_id = None


def handle_exception(exception: Exception) -> None:
    for handler in exception_handlers:
        result = handler() if not inspect.signature(handler).parameters else handler(exception)
        if isinstance(result, Awaitable):
            background_tasks.create(result)
