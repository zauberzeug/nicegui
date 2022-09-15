from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Awaitable, Callable, Dict, List, Union

from uvicorn import Server

if TYPE_CHECKING:
    import justpy as jp
    from starlette.applications import Starlette

    from .config import Config
    from .elements.page import PageBuilder

app: 'Starlette'
config: 'Config'
server: Server
page_builders: Dict[str, 'PageBuilder'] = {}
view_stack: List['jp.HTMLBaseComponent'] = []
tasks: List[asyncio.tasks.Task] = []
log: logging.Logger = logging.getLogger('nicegui')
connect_handlers: List[Union[Callable, Awaitable]] = []
disconnect_handlers: List[Union[Callable, Awaitable]] = []
startup_handlers: List[Union[Callable, Awaitable]] = []
shutdown_handlers: List[Union[Callable, Awaitable]] = []
pre_evaluation_succeeded: bool = False


def find_route(function: Callable) -> str:
    routes = [route for route, page_builder in page_builders.items() if page_builder.function == function]
    if not routes:
        raise ValueError(f'Invalid page function {function}')
    return routes[0]
