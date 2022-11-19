import asyncio
import logging
from enum import Enum
from typing import TYPE_CHECKING, Awaitable, Callable, Dict, List, Optional, Union

from fastapi import FastAPI
from socketio import AsyncServer

if TYPE_CHECKING:
    from .client import Client


class State(Enum):
    STOPPED = 0
    STARTING = 1
    STARTED = 2
    STOPPING = 3


app: FastAPI
sio: AsyncServer
loop: Optional[asyncio.AbstractEventLoop] = None
log: logging.Logger = logging.getLogger('nicegui')
state: State = State.STOPPED

host: str
port: int
dark: Optional[bool] = False
binding_refresh_interval: float

client_stack: List['Client'] = []
clients: Dict[int, 'Client'] = {}
next_client_id: int = 0

page_routes: Dict[Callable, str] = {}
tasks: List[asyncio.tasks.Task] = []

connect_handlers: List[Union[Callable, Awaitable]] = []
disconnect_handlers: List[Union[Callable, Awaitable]] = []
startup_handlers: List[Union[Callable, Awaitable]] = []
shutdown_handlers: List[Union[Callable, Awaitable]] = []
