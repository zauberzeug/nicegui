from typing import List

from nicegui import Client, ui

from .screen import Screen


def test_adding_elements_during_onconnect_on_auto_index_page(screen: Screen):
    connections = []
    ui.label('Adding labels on_connect')
    ui.lifecycle.on_connect(lambda _: connections.append(ui.label(f'new connection {len(connections)}')))

    screen.open('/')
    screen.should_contain('new connection 0')
    screen.open('/')
    screen.should_contain('new connection 0')
    screen.should_contain('new connection 1')
    screen.open('/')
    screen.should_contain('new connection 0')
    screen.should_contain('new connection 1')
    screen.should_contain('new connection 2')


def test_async_connect_handler(screen: Screen):
    async def run_js():
        result.text = await ui.run_javascript('41 + 1')
    result = ui.label()
    ui.lifecycle.on_connect(run_js)

    screen.open('/')
    screen.should_contain('42')


def test_connect_disconnect_is_called_for_each_client(screen: Screen):
    events: List[str] = []

    @ui.page('/')
    def page(client: Client):
        ui.label(f'client id: {client.id}')
    ui.lifecycle.on_connect(lambda: events.append('connect'))
    ui.lifecycle.on_disconnect(lambda: events.append('disconnect'))

    screen.open('/')
    screen.wait(0.5)
    screen.open('/')
    screen.wait(0.5)
    screen.open('/')
    screen.wait(0.5)
    assert events == ['connect', 'disconnect', 'connect', 'disconnect', 'connect']
