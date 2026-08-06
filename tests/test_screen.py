import httpx

from nicegui import helpers, ui
from nicegui.testing import Screen


def test_start_server_waits_until_the_port_is_open(screen: Screen):
    @ui.page('/')
    def page():
        ui.label('Hello')

    screen.start_server()
    assert helpers.is_port_open('localhost', Screen.PORT)
    assert httpx.get(f'http://localhost:{Screen.PORT}/').status_code == 200
