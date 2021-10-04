from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from starlette.applications import Starlette
    import justpy as jp
    from .config import Config
    from .elements.page import Page

app: 'Starlette'
config: 'Config'
page_stack: list['Page'] = []
view_stack: list['jp.HTMLBaseComponent'] = []
