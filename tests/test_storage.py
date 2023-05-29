import asyncio
from uuid import uuid4

from nicegui import Client, app, ui

from .screen import Screen


def test_session_data_is_stored_in_the_browser(screen: Screen):
    @ui.page('/')
    def page():
        app.storage.session['count'] = app.storage.session.get('count', 0) + 1
        ui.label(app.storage.session['count'] or 'no session')

    @app.get('/session')
    def session():
        return 'count = ' + str(app.storage.session['count'])

    screen.open('/')
    screen.should_contain('1')
    screen.open('/')
    screen.should_contain('2')
    screen.open('/')
    screen.should_contain('3')
    screen.open('/session')
    screen.should_contain('count = 3')


def test_session_storage_supports_asyncio(screen: Screen):
    @ui.page('/')
    async def page():
        app.storage.session['count'] = app.storage.session.get('count', 0) + 1
        await asyncio.sleep(0.5)
        ui.label(app.storage.session['count'] or 'no session')

    screen.open('/')
    screen.switch_to(1)
    screen.open('/')
    screen.should_contain('2')
    screen.switch_to(0)
    screen.open('/')
    screen.should_contain('3')


def test_session_modifications_after_page_load(screen: Screen):
    random_data = str(uuid4())

    @ui.page('/')
    async def page(client: Client):
        await client.connected()
        app.storage.session['test'] = random_data

    screen.open('/')
    screen.should_contain(random_data)
