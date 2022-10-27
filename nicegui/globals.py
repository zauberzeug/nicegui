from __future__ import annotations

import asyncio
import logging
from enum import Enum
from typing import TYPE_CHECKING, Awaitable, Callable, Dict, List, Optional, Union

from starlette.applications import Starlette
from uvicorn import Server

from .config import Config

if TYPE_CHECKING:
    import justpy as jp

    from .page_builder import PageBuilder


class State(Enum):
    STOPPED = 0
    STARTING = 1
    STARTED = 2
    STOPPING = 3


app: Starlette
config: Optional[Config] = None
server: Optional[Server] = None
state: State = State.STOPPED
loop: Optional[asyncio.AbstractEventLoop] = None
page_builders: Dict[str, 'PageBuilder'] = {}
view_stacks: Dict[int, List['jp.HTMLBaseComponent']] = {}
tasks: List[asyncio.tasks.Task] = []
log: logging.Logger = logging.getLogger('nicegui')
connect_handlers: List[Union[Callable, Awaitable]] = []
disconnect_handlers: List[Union[Callable, Awaitable]] = []
startup_handlers: List[Union[Callable, Awaitable]] = []
shutdown_handlers: List[Union[Callable, Awaitable]] = []


def find_route(function: Callable) -> str:
    routes = [route for route, page_builder in page_builders.items() if page_builder.function == function]
    if not routes:
        raise ValueError(f'Invalid page function {function}')
    return routes[0]
