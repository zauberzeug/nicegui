from typing import List

from nicegui import app, ui
from nicegui.testing import SeleniumScreen


def test_adding_elements_during_onconnect_on_auto_index_page(screen: SeleniumScreen):
    connections = []
    ui.label('Adding labels on_connect')
    app.on_connect(lambda _: connections.append(ui.label(f'new connection {len(connections)}')))

    screen.open('/')
    screen.should_contain('new connection 0')
    screen.open('/')
    screen.should_contain('new connection 0')
    screen.should_contain('new connection 1')
    screen.open('/')
    screen.should_contain('new connection 0')
    screen.should_contain('new connection 1')
    screen.should_contain('new connection 2')


def test_async_connect_handler(screen: SeleniumScreen):
    async def run_js():
        result.text = await ui.run_javascript('41 + 1')
    result = ui.label()
    app.on_connect(run_js)

    screen.open('/')
    screen.should_contain('42')


def test_connect_disconnect_is_called_for_each_client(screen: SeleniumScreen):
    events: List[str] = []

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


def test_startup_and_shutdown_handlers(screen: SeleniumScreen):
    events: List[str] = []

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

    screen.open('/')
    screen.wait(0.5)
    assert events == ['startup', 'startup_async', 'startup_async']

    app.shutdown()
    screen.wait(0.5)
    assert events == ['startup', 'startup_async', 'startup_async', 'shutdown', 'shutdown_async', 'shutdown_async']
