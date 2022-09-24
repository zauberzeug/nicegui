import asyncio
from uuid import uuid4

from nicegui import task_logger, ui

from .user import User


def test_page(user: User):
    @ui.page('/')
    def page():
        ui.label('Hello, world!')

    user.open('/')
    user.should_see('NiceGUI')
    user.should_see('Hello, world!')


def test_shared_page(user: User):
    @ui.page('/', shared=True)
    def page():
        ui.label('Hello, world!')

    user.open('/')
    user.should_see('NiceGUI')
    user.should_see('Hello, world!')


def test_auto_index_page(user: User):
    ui.label('Hello, world!')

    user.open('/')
    user.should_see('NiceGUI')
    user.should_see('Hello, world!')


def test_custom_title(user: User):
    @ui.page('/', title='My Custom Title')
    def page():
        ui.label('Hello, world!')

    user.open('/')
    user.should_see('My Custom Title')
    user.should_see('Hello, world!')


def test_route_with_custom_path(user: User):
    @ui.page('/test_route')
    def page():
        ui.label('page with custom path')

    user.open('/test_route')
    user.should_see('page with custom path')


def test_auto_index_page_with_link_to_subpage(user: User):
    ui.link('link to subpage', '/subpage')

    @ui.page('/subpage')
    def page():
        ui.label('the subpage')

    user.open('/')
    user.click('link to subpage')
    user.should_see('the subpage')


def test_link_to_page_by_passing_function(user: User):
    @ui.page('/subpage')
    def page():
        ui.label('the subpage')

    ui.link('link to subpage', page)

    user.open('/')
    user.click('link to subpage')
    user.should_see('the subpage')


def test_creating_new_page_after_startup(user: User):
    user.start_server()

    @ui.page('/late_page')
    def page():
        ui.label('page created after startup')

    user.open('/late_page')
    user.should_see('page created after startup')


def test_shared_and_individual_pages(user: User):
    @ui.page('/individual_page')
    def individual_page():
        ui.label(f'individual page with uuid {uuid4()}')

    @ ui.page('/shared_page', shared=True)
    def shared_page():
        ui.label(f'shared page with uuid {uuid4()}')

    user.open('/shared_page')
    uuid1 = user.find('shared page').text.split()[-1]
    user.open('/shared_page')
    uuid2 = user.find('shared page').text.split()[-1]
    assert uuid1 == uuid2

    user.open('/individual_page')
    uuid1 = user.find('individual page').text.split()[-1]
    user.open('/individual_page')
    uuid2 = user.find('individual page').text.split()[-1]
    assert uuid1 != uuid2


def test_on_page_ready_event(user: User):
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

    user.open('/')
    user.should_see('delayed data has been loaded')
