import asyncio

from nicegui import ui
from nicegui.testing import Screen

# pylint: disable=missing-docstring


def test_routing_url(screen: Screen):
    @ui.outlet('/', on_navigate=lambda _: '/main')
    def layout():
        ui.label('main layout')
        yield

    @layout.view('/main')
    def main_content():
        ui.label('main content')

    screen.open('/')
    screen.should_contain('main layout')
    screen.should_contain('main content')
    assert '/main' in screen.selenium.current_url


def test_passing_objects_via_yield(screen: Screen):
    @ui.outlet('/')
    def layout():
        title = ui.label('original title')
        yield {'title': title}

    @layout.view('/')
    def main_content(title: ui.label):
        title.set_text('changed title')

    screen.open('/')
    screen.should_contain('changed title')


def test_async_outlet(screen: Screen):
    @ui.outlet('/')
    async def layout():
        ui.label('main layout')
        await asyncio.sleep(0.2)
        ui.label('delayed content')
        yield
        ui.label('after yield')

    screen.open('/')
    screen.should_contain('main layout')
    screen.should_contain('delayed content')
    screen.should_contain('after yield')


def test_outlet_with_async_sub_outlet(screen: Screen):
    @ui.outlet('/')
    def layout():
        ui.label('main')
        yield

    @layout.outlet('/')
    async def main_content():
        await asyncio.sleep(0.2)
        ui.label('sub')
        yield

    screen.open('/')
    screen.should_contain('main')
    screen.should_contain('sub')
