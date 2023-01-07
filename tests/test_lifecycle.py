from typing import List

from nicegui import Client, ui

from .screen import Screen


def test_adding_elements_during_onconnect_on_auto_index_page(screen: Screen):
    connections = []
    ui.label('Adding labels on_connect')
    ui.on_connect(lambda _: connections.append(ui.label(f'new connection {len(connections)}')))

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
    async def run_js(client: Client):
        result.text = await ui.run_javascript('41 + 1')
    result = ui.label()
    ui.on_connect(run_js)

    screen.open('/')
    screen.should_contain('42')


def test_connect_disconnect_is_called_for_each_client(screen: Screen):
    events: List[str] = []

    @ui.page('/')
    def page(client: Client):
        ui.label(f'client id: {client.id}')
    ui.on_connect(lambda c: events.append(f'|connect {c.id}|'))
    ui.on_disconnect(lambda c: events.append(f'|disconnect {c.id}|'))

    screen.open('/')
    screen.open('/')
    screen.open('/')
    screen.wait(0.1)
    assert len(events) == 5
    assert events[0].startswith('|connect ')
    assert events[1].startswith('|disconnect ')
    assert events[2].startswith('|connect ')
    assert events[3].startswith('|disconnect ')
    assert events[4].startswith('|connect ')
