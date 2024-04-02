from typing import Any, Callable

from fastapi.routing import APIRoute
from starlette.routing import Route

from nicegui import ui
from nicegui.page_builder import PageBuilder, PageRouter
from nicegui.single_page import SinglePageRouter
from nicegui import core

from sub_page import sub_page


@ui.page('/some_page')
def some_page():
    ui.label('Some Page').classes('text-2xl')


sp = SinglePageRouter("/")
ui.run(show=False)
