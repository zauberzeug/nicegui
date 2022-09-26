import asyncio
from tkinter import N
from uuid import uuid4

import justpy.htmlcomponents
from nicegui import task_logger, ui

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

    @ ui.page('/shared_page', shared=True)
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

    async def load():
        label.text = 'loading...'
        # NOTE we can not use asyncio.create_task() here because we are on a different thread than the nicegui event loop
        task_logger.create_task(takes_a_while())

    async def takes_a_while():
        await asyncio.sleep(0.1)
        label.text = 'delayed data has been loaded'

    @ui.page('/', on_page_ready=load)
    def page():
        global label
        label = ui.label()

    screen.open('/')
    screen.should_contain('delayed data has been loaded')


def test_customised_page(screen: Screen):
    trace = []

    class custom_page(ui.page):

        def __init__(self, route: str, **kwargs):
            super().__init__(route, title='My Customized Page', **kwargs)
            trace.append('init')

        async def header(self) -> None:
            assert isinstance(self.page.view, justpy.htmlcomponents.Div), \
                'we should be able to access the underlying justpy view'
            await super().header()
            trace.append('header')

        async def footer(self) -> None:
            await super().footer()
            trace.append('footer')

    @custom_page('/', dark=True)
    def mainpage():
        trace.append('content')
        ui.label('Hello, world!')

    screen.open('/')
    screen.should_contain('Hello, world!')
    screen.should_contain('My Customized Page')
    assert 'body--dark' in screen.get_tags('body')[0].get_attribute('class')
    assert trace == ['init', 'header', 'content', 'footer']
