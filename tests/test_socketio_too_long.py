import re
from typing import Literal

import pytest
from selenium.webdriver.common.keys import Keys

from nicegui import core, ui
from nicegui.testing import Screen

PAYLOAD_RE = re.compile(r'Payload size \d+ exceeds the maximum allowed limit\.')


@pytest.mark.parametrize('transport,overhead', [('websocket', 262), ('polling', 250_240)])
def test_socketio_too_long(screen: Screen, transport: Literal['websocket', 'polling'], overhead: int):
    events: list[str] = []
    core.app.config.socket_io_js_transports = [transport]

    @ui.page('/')
    def page():
        ui.textarea(value='x' * (1_000_000 - overhead), on_change=lambda: events.append('changed'))

    screen.open('/')
    screen.type(Keys.TAB)
    for _ in range(5):
        screen.type('y')

    assert events == ['changed'] * 2, 'two more characters are ok'
    assert len([log for log in screen.selenium.get_log('browser') if 'Payload size' in log['message']]) == 3
    screen.assert_py_logger('ERROR', PAYLOAD_RE)
    screen.assert_py_logger('ERROR', PAYLOAD_RE)
    screen.assert_py_logger('ERROR', PAYLOAD_RE)
