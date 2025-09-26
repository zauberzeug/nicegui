import asyncio

from nicegui import app, ui
from nicegui.testing import Screen


def test_adding_elements_during_onconnect_on_auto_index_page(screen: Screen):
    connections = {'count': 0}
    app.on_connect(lambda _: connections.update(count=connections['count'] + 1))

    @ui.page('/')
    def page():
        ui.label('Hello')

    screen.open('/')
    screen.should_contain('Hello')
    assert connections['count'] == 1

    screen.open('/')
    screen.should_contain('Hello')
    assert connections['count'] == 2

    screen.open('/')
    screen.should_contain('Hello')
    assert connections['count'] == 3


def test_async_connect_handler(screen: Screen):
    connections = {'count': 0}

    @app.on_connect
    async def handle_connect():
        await asyncio.sleep(0.1)
        connections.update(count=connections['count'] + 1)

    @ui.page('/')
    def page():
        ui.label('Hello')

    screen.open('/')
    screen.should_contain('Hello')
    screen.wait(0.5)
    assert connections['count'] == 1

    screen.open('/')
    screen.should_contain('Hello')
    screen.wait(0.5)
    assert connections['count'] == 2

    screen.open('/')
    screen.should_contain('Hello')
    screen.wait(0.5)
    assert connections['count'] == 3


def test_connect_disconnect_is_called_for_each_client(screen: Screen):
    events: list[str] = []

    @ui.page('/', reconnect_timeout=0)
    def page():
        ui.label(f'client id: {ui.context.client.id}')
    app.on_connect(lambda: events.append('connect'))
    app.on_disconnect(lambda: events.append('disconnect'))

    screen.open('/')
    screen.wait(0.5)
    screen.open('/')
    screen.wait(0.5)
    screen.open('/')
    screen.wait(0.5)
    assert events == ['connect', 'disconnect', 'connect', 'disconnect', 'connect']


def test_startup_and_shutdown_handlers(screen: Screen):
    events: list[str] = []

    def startup():
        events.append('startup')

    async def startup_async():
        events.append('startup_async')

    def shutdown():
        events.append('shutdown')

    async def shutdown_async():
        events.append('shutdown_async')

    app.on_startup(startup)
    app.on_startup(startup_async)
    app.on_startup(startup_async())
    app.on_shutdown(shutdown)
    app.on_shutdown(shutdown_async)
    app.on_shutdown(shutdown_async())

    @ui.page('/')
    def page():
        ui.label('Hello')

    screen.open('/')
    screen.wait(0.5)
    assert events == ['startup', 'startup_async', 'startup_async']

    app.shutdown()
    screen.wait(0.5)
    assert events == ['startup', 'startup_async', 'startup_async', 'shutdown', 'shutdown_async', 'shutdown_async']


def test_all_lifecycle_handlers_are_called(screen: Screen):
    events: list[str] = []

    app.on_connect(lambda: events.append('app connect'))
    app.on_disconnect(lambda: events.append('app disconnect'))
    app.on_delete(lambda: events.append('app delete'))

    @ui.page('/')
    def page():
        ui.context.client.on_connect(lambda: events.append('page connect'))
        ui.context.client.on_disconnect(lambda: events.append('page disconnect'))
        ui.context.client.on_delete(lambda: events.append('page delete'))

        ui.button('Delete', on_click=ui.context.client.delete)

    screen.open('/')
    screen.wait(0.5)
    assert events == ['page connect', 'app connect']

    screen.selenium.execute_script('window.socket.disconnect();')
    screen.wait(0.5)
    assert events == ['page connect', 'app connect',
                      'page disconnect', 'app disconnect']

    screen.selenium.execute_script('window.socket.connect();')
    screen.wait(0.5)
    assert events == ['page connect', 'app connect',
                      'page disconnect', 'app disconnect',
                      'page connect', 'app connect']

    screen.click('Delete')
    screen.wait(0.5)
    assert events == ['page connect', 'app connect',
                      'page disconnect', 'app disconnect',
                      'page connect', 'app connect',
                      'page delete', 'app delete']
