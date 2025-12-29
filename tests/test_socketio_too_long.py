import pytest
from selenium.webdriver.common.keys import Keys
from typing_extensions import Literal

from nicegui import core, ui
from nicegui.testing import Screen


@pytest.mark.parametrize('transport', ['websocket', 'polling'])
def test_socketio_too_long(screen: Screen, transport: Literal['websocket', 'polling']):
    events: list[str] = []
    core.app.config.socket_io_js_transports = [transport]

    @ui.page('/')
    def page():
        ui.textarea(value='x' * (1_000_000 - 242), on_change=lambda: events.append('changed'))

    screen.open('/')
    screen.type(Keys.TAB)
    for _ in range(5):
        screen.type('y')

    assert events == ['changed'] * 2, 'two more characters are ok'
    assert len([log for log in screen.selenium.get_log('browser') if 'Payload size' in log['message']]) == 3
