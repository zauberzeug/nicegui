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
    screen.wait(1.0)
    screen.should_contain('main layout')
    screen.should_contain('main content')
    assert screen.selenium.current_url.split('/')[-1] == ''  # just the content should have changed, not the url


def test_routing_url_w_forward(screen: Screen):
    def handle_navigate(url: str):
        if url == '/':
            ui.navigate.to('/main')
            return None  # prevent providing new content, forward to the new url
        return url

    @ui.outlet('/', on_navigate=handle_navigate)
    def layout():
        ui.label('main layout')
        yield

    @layout.view('/main')
    def main_content():
        ui.label('main content')

    screen.open('/')
    screen.wait(1.0)
    screen.should_contain('main layout')
    screen.should_contain('main content')
    assert screen.selenium.current_url.split('/')[-1] == 'main'  # just the content should have changed, not the url


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


def test_query_parameters_persistence(screen: Screen):
    received_params = {}

    @ui.outlet('/')
    def layout():
        ui.label('layout')
        yield

    @layout.view('/')
    def index():
        ui.label('index')
        ui.link('Go to page with params', '/page?param1=value1&param2=value2')

    @layout.view('/page')
    def page(param1: str = '', param2: str = ''):
        # Store the raw values for assertion
        received_params.clear()  # Clear previous values to avoid state issues
        received_params['param1'] = param1
        received_params['param2'] = param2
        ui.label(f'params: {param1}, {param2}')
        ui.link('Go to other', '/other')

    @layout.view('/other')
    def other():
        ui.label('other page')

    # Navigate to index
    screen.open('/')
    screen.should_contain('index')

    # Click link to page with parameters
    screen.click('Go to page with params')
    screen.should_contain('params: value1, value2')
    assert received_params['param1'] == 'value1'
    assert received_params['param2'] == 'value2'
    assert 'param1=value1' in screen.selenium.current_url
    assert 'param2=value2' in screen.selenium.current_url

    # Navigate to other page
    screen.click('Go to other')
    screen.should_contain('other page')
    assert 'param1' not in screen.selenium.current_url
    assert 'param2' not in screen.selenium.current_url

    # Go back and verify parameters are preserved
    screen.selenium.back()
    screen.wait(0.5)  # wait for navigation to complete
    screen.should_contain('params: value1, value2')
    assert received_params['param1'] == 'value1'
    assert received_params['param2'] == 'value2'
    assert 'param1=value1' in screen.selenium.current_url
    assert 'param2=value2' in screen.selenium.current_url


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
