import asyncio
import logging
from contextlib import contextmanager
from enum import Enum
from typing import TYPE_CHECKING, Awaitable, Callable, Dict, List, Optional, Union

from fastapi import FastAPI
from socketio import AsyncServer
from uvicorn import Server

if TYPE_CHECKING:
    from .client import Client
    from .slot import Slot


class State(Enum):
    STOPPED = 0
    STARTING = 1
    STARTED = 2
    STOPPING = 3


app: FastAPI
sio: AsyncServer
server: Server
loop: Optional[asyncio.AbstractEventLoop] = None
log: logging.Logger = logging.getLogger('nicegui')
state: State = State.STOPPED

host: str
port: int
reload: bool
title: str
favicon: Optional[str]
dark: Optional[bool]
binding_refresh_interval: float
excludes: List[str]
socket_io_js_extra_headers: Dict = {}

_socket_id: Optional[str] = None
slot_stacks: Dict[int, List['Slot']] = {}
clients: Dict[str, 'Client'] = {}
index_client: 'Client'

page_routes: Dict[Callable, str] = {}
tasks: List[asyncio.tasks.Task] = []

startup_handlers: List[Union[Callable, Awaitable]] = []
shutdown_handlers: List[Union[Callable, Awaitable]] = []


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
def socket_id(id: str) -> None:
    global _socket_id
    _socket_id = id
    yield
    _socket_id = None
