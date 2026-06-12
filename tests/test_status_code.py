import httpx

from nicegui import ui
from nicegui.testing import Screen


def test_status_code(screen: Screen):
    @ui.page('/')
    def page():
        ui.status_code(404)
        ui.label('not found')

    screen.start_server()
    assert httpx.get(f'http://localhost:{Screen.PORT}/').status_code == 404


def test_default_status_code(screen: Screen):
    @ui.page('/')
    def page():
        ui.label('hello')

    screen.start_server()
    assert httpx.get(f'http://localhost:{Screen.PORT}/').status_code == 200
