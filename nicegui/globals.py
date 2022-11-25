import asyncio
import logging
from enum import Enum
from typing import TYPE_CHECKING, Awaitable, Callable, Dict, List, Optional, Union

from fastapi import FastAPI
from socketio import AsyncServer
from uvicorn import Server

if TYPE_CHECKING:
    from .client import Client


class State(Enum):
    STOPPED = 0
    STARTING = 1
    STARTED = 2
    STOPPING = 3


app: FastAPI
sio: AsyncServer
server: Optional[Server] = None
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

client_stacks: Dict[int, List['Client']] = {}
clients: Dict[int, 'Client'] = {}
next_client_id: int = 0

page_routes: Dict[Callable, str] = {}
favicons: Dict[str, Optional[str]] = {}
tasks: List[asyncio.tasks.Task] = []

connect_handlers: List[Union[Callable, Awaitable]] = []
disconnect_handlers: List[Union[Callable, Awaitable]] = []
startup_handlers: List[Union[Callable, Awaitable]] = []
shutdown_handlers: List[Union[Callable, Awaitable]] = []


def get_task_id() -> int:
    return id(asyncio.current_task()) if loop and loop.is_running() else 0


def get_client_stack() -> List['Client']:
    task_id = get_task_id()
    if task_id not in client_stacks:
        client_stacks[task_id] = []
    return client_stacks[task_id]


def get_client() -> 'Client':
    return get_client_stack()[-1]
