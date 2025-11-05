import asyncio

from nicegui import ui
from nicegui.testing import Screen


def test_root_page(screen: Screen):
    def root():
        ui.label('Hello, World!')

    screen.ui_run_kwargs['root'] = root
    screen.open('/')
    screen.should_contain('Hello, World!')


def test_async_root_page(screen: Screen):
    async def root():
        await asyncio.sleep(0.1)
        ui.label('Hello, World!')

    screen.ui_run_kwargs['root'] = root
    screen.open('/')
    screen.should_contain('Hello, World!')


def test_root_page_with_query_parameters(screen: Screen):
    def root(x: int = 0):
        ui.label(f'{x = }')

    screen.ui_run_kwargs['root'] = root
    screen.open('/')
    screen.should_contain('x = 0')

    screen.open('/?x=42')
    screen.should_contain('x = 42')


def test_root_page_with_request_injection(screen: Screen):
    from fastapi import Request

    def root(request: Request):
        ui.label(f'path: {request.url.path}')
        ui.label(f'name: {request.query_params.get("name", "unknown")}')

    screen.ui_run_kwargs['root'] = root
    screen.open('/')
    screen.should_contain('path: /')
    screen.should_contain('name: unknown')

    screen.open('/?name=test')
    screen.should_contain('path: /')
    screen.should_contain('name: test')
