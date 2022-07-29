from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Awaitable, Callable, List, Union

if TYPE_CHECKING:
    import justpy as jp
    from starlette.applications import Starlette

    from .config import Config
    from .elements.page import Page

app: 'Starlette'
config: 'Config'
page_stack: List['Page'] = []
view_stack: List['jp.HTMLBaseComponent'] = []
tasks: List[asyncio.tasks.Task] = []
log: logging.Logger = logging.getLogger('nicegui')
connect_handlers: List[Union[Callable, Awaitable]] = []
disconnect_handlers: List[Union[Callable, Awaitable]] = []
startup_handlers: List[Union[Callable, Awaitable]] = []
shutdown_handlers: List[Union[Callable, Awaitable]] = []
