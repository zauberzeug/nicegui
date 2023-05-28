import requests

from nicegui import app, globals, ui

from .screen import PORT, Screen


def test_session_data_is_stored_in_the_browser(screen: Screen):
    @ui.page('/')
    def page():
        ui.session.get()['count'] = ui.session.get().get('count', 0) + 1
        ui.label(ui.session.get()['count'] or 'no session')

    @app.get('/session')
    def session():
        return 'count = ' + str(ui.session.get()['count'])

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
        ui.session.get()['count'] = ui.session.get().get('count', 0) + 1
        await asyncio.sleep(0.5)
        ui.label(ui.session.get()['count'] or 'no session')

    screen.open('/')
    screen.switch_to(1)
    screen.open('/')
    screen.should_contain('2')
    screen.switch_to(0)
    screen.open('/')
    screen.should_contain('3')

    #     ui.input('name').bind_value(request.session, 'key')

    # screen.open('/')
    # screen.find('input').send_keys('some text')
    # screen.open('/')
    # screen.should_contain('some text')
