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
