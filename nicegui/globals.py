from __future__ import annotations

import asyncio
import logging
from contextlib import contextmanager
from enum import Enum
from typing import TYPE_CHECKING, Awaitable, Callable, Dict, Generator, List, Optional, Union

from starlette.applications import Starlette
from uvicorn import Server

from .config import Config
from .task_logger import create_task

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


def get_task_id() -> int:
    return id(asyncio.current_task()) if loop and loop.is_running() else 0


def get_view_stack() -> List['jp.HTMLBaseComponent']:
    task_id = get_task_id()
    if task_id not in view_stacks:
        view_stacks[task_id] = []
    return view_stacks[task_id]


def prune_view_stack() -> None:
    task_id = get_task_id()
    if not view_stacks[task_id]:
        del view_stacks[task_id]


@contextmanager
def within_view(view: 'jp.HTMLBaseComponent') -> Generator[None, None, None]:
    child_count = len(view)
    get_view_stack().append(view)
    yield
    get_view_stack().pop()
    prune_view_stack()
    if len(view) != child_count:
        create_task(view.update())
