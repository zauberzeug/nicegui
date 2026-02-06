from typing import Literal

import pytest
from selenium.webdriver.common.keys import Keys

from nicegui import core, ui
from nicegui.testing import SharedScreen


@pytest.mark.parametrize('transport', ['websocket', 'polling'])
def test_socketio_too_long(shared_screen: SharedScreen, transport: Literal['websocket', 'polling']):
    events: list[str] = []
    core.app.config.socket_io_js_transports = [transport]

    @ui.page('/')
    def page():
        ui.textarea(value='x' * (1_000_000 - 242), on_change=lambda: events.append('changed'))

    shared_screen.open('/')
    shared_screen.type(Keys.TAB)
    for _ in range(5):
        shared_screen.type('y')

    assert events == ['changed'] * 2, 'two more characters are ok'
    assert len([log for log in shared_screen.selenium.get_log('browser') if 'Payload size' in log['message']]) == 3
    shared_screen.assert_py_logger('ERROR', 'Payload size 999901 exceeds the maximum allowed limit.')
    shared_screen.assert_py_logger('ERROR', 'Payload size 999902 exceeds the maximum allowed limit.')
    shared_screen.assert_py_logger('ERROR', 'Payload size 999903 exceeds the maximum allowed limit.')
