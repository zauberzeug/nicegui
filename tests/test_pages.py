import asyncio
from time import time
from typing import Generator
from uuid import uuid4

import justpy.htmlcomponents
from nicegui import task_logger, ui
from nicegui.events import PageEvent
from starlette.requests import Request

from .screen import Screen


def test_page(screen: Screen):
    @ui.page('/')
    def page():
        ui.label('Hello, world!')

    screen.open('/')
    screen.should_contain('NiceGUI')
    screen.should_contain('Hello, world!')


def test_shared_page(screen: Screen):
    @ui.page('/', shared=True)
    def page():
        ui.label('Hello, world!')

    screen.open('/')
    screen.should_contain('NiceGUI')
    screen.should_contain('Hello, world!')


def test_auto_index_page(screen: Screen):
    ui.label('Hello, world!')

    screen.open('/')
    screen.should_contain('NiceGUI')
    screen.should_contain('Hello, world!')


def test_custom_title(screen: Screen):
    @ui.page('/', title='My Custom Title')
    def page():
        ui.label('Hello, world!')

    screen.open('/')
    screen.should_contain('My Custom Title')
    screen.should_contain('Hello, world!')


def test_route_with_custom_path(screen: Screen):
    @ui.page('/test_route')
    def page():
        ui.label('page with custom path')

    screen.open('/test_route')
    screen.should_contain('page with custom path')


def test_auto_index_page_with_link_to_subpage(screen: Screen):
    ui.link('link to subpage', '/subpage')

    @ui.page('/subpage')
    def page():
        ui.label('the subpage')

    screen.open('/')
    screen.click('link to subpage')
    screen.should_contain('the subpage')


def test_link_to_page_by_passing_function(screen: Screen):
    @ui.page('/subpage')
    def page():
        ui.label('the subpage')

    ui.link('link to subpage', page)

    screen.open('/')
    screen.click('link to subpage')
    screen.should_contain('the subpage')


def test_creating_new_page_after_startup(screen: Screen):
    screen.start_server()

    @ui.page('/late_page')
    def page():
        ui.label('page created after startup')

    screen.open('/late_page')
    screen.should_contain('page created after startup')


def test_shared_and_individual_pages(screen: Screen):
    @ui.page('/individual_page')
    def individual_page():
        ui.label(f'individual page with uuid {uuid4()}')

    @ui.page('/shared_page', shared=True)
    def shared_page():
        ui.label(f'shared page with uuid {uuid4()}')

    screen.open('/shared_page')
    uuid1 = screen.find('shared page').text.split()[-1]
    screen.open('/shared_page')
    uuid2 = screen.find('shared page').text.split()[-1]
    assert uuid1 == uuid2

    screen.open('/individual_page')
    uuid1 = screen.find('individual page').text.split()[-1]
    screen.open('/individual_page')
    uuid2 = screen.find('individual page').text.split()[-1]
    assert uuid1 != uuid2


def test_on_page_ready_event(screen: Screen):
    '''This feature was introduced to fix #50; see https://github.com/zauberzeug/nicegui/issues/50#issuecomment-1210962617.'''

    async def load() -> None:
        label.text = 'loading...'
        # NOTE we can not use asyncio.create_task() here because we are on a different thread than the nicegui event loop
        task_logger.create_task(takes_a_while())

    async def takes_a_while() -> None:
        await asyncio.sleep(0.1)
        label.text = 'delayed data has been loaded'

    @ui.page('/', on_page_ready=load)
    def page():
        global label
        label = ui.label()

    screen.open('/')
    screen.should_contain('delayed data has been loaded')


def test_customized_page(screen: Screen):
    trace = []

    class custom_page(ui.page):

        def __init__(self, route: str, **kwargs):
            super().__init__(route, title='My Customized Page', **kwargs)
            trace.append('init')

        async def connected(self, request: Request) -> None:
            await super().connected(request)
            assert isinstance(request, Request)
            trace.append('connected')

        async def before_content(self) -> None:
            assert isinstance(self.page.view, justpy.htmlcomponents.Div), \
                'we should be able to access the underlying JustPy view'
            await super().before_content()
            trace.append('before_content')

        async def after_content(self) -> None:
            await super().after_content()
            trace.append('after_content')

    @custom_page('/', dark=True)
    def mainpage():
        trace.append('content')
        ui.label('Hello, world!')

    screen.open('/')
    screen.should_contain('Hello, world!')
    screen.should_contain('My Customized Page')
    assert 'body--dark' in screen.get_tags('body')[0].get_attribute('class')
    assert trace == ['init', 'connected', 'before_content', 'content', 'after_content']


def test_shared_page_with_request_parameter_raises_exception(screen: Screen):
    @ui.page('/', shared=True)
    def page(request: Request):
        ui.label('Hello, world!')

    screen.open('/')
    screen.should_contain('500')
    screen.should_contain('Server error')
    screen.assert_py_logger('ERROR', 'Cannot use `request` argument in shared page')


def test_adding_elements_in_on_page_ready_event(screen: Screen):
    @ui.page('/', on_page_ready=lambda: ui.markdown('Hello, world!'))
    def page():
        pass

    screen.open('/')
    screen.should_contain('Hello, world!')


def test_pageready_after_yield_on_async_page(screen: Screen):
    @ui.page('/')
    async def page() -> Generator[None, PageEvent, None]:
        ui.label('before')
        page_ready = yield
        await asyncio.sleep(1)
        ui.label('after')
        ui.label(page_ready.socket.base_url)

    screen.open('/')
    screen.should_contain('before')
    screen.should_not_contain('after')
    screen.wait(1)
    screen.should_contain('after')
    screen.should_contain('ws://localhost:3392/')


def test_pageready_after_yield_on_non_async_page(screen: Screen):
    @ui.page('/')
    def page() -> Generator[None, PageEvent, None]:
        t = time()
        page_ready = yield
        ui.label(f'loading page took {time() - t:.2f} seconds')
        ui.label(page_ready.socket.base_url)

    screen.open('/')
    timing = screen.find('loading page took')
    assert 0 < float(timing.text.split()[-2]) < 3
    screen.should_contain('ws://localhost:3392/')


def test_pageready_after_yield_on_shared_page_raises_exception(screen: Screen):
    @ui.page('/', shared=True)
    def page():
        yield

    screen.open('/')
    screen.should_contain('500')
    screen.should_contain('Server error')
    screen.assert_py_logger('ERROR', 'Yielding for page_ready is not supported on shared pages')


def test_exception_before_yield_on_async_page(screen: Screen):
    @ui.page('/')
    async def page() -> Generator[None, PageEvent, None]:
        raise Exception('some exception')

    screen.open('/')
    screen.should_contain('500')
    screen.should_contain('Server error')
    screen.assert_py_logger('ERROR', 'some exception')


def test_exception_after_yield_on_async_page(screen: Screen):
    @ui.page('/')
    async def page() -> Generator[None, PageEvent, None]:
        yield
        ui.label('this is shown')
        raise Exception('some exception')

    screen.open('/')
    screen.should_contain('this is shown')
    screen.assert_py_logger('ERROR', 'Failed to execute page-ready')


def test_exception_in_on_page_ready_callback(screen: Screen):
    def ready():
        raise Exception('some exception')

    @ui.page('/', on_page_ready=ready)
    async def page() -> None:
        ui.label('this is shown')

    screen.open('/')
    screen.should_contain('this is shown')
    screen.assert_py_logger('ERROR', 'Failed to execute page-ready')
