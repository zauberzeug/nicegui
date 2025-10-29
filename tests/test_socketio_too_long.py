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

    # first 2 times OK
    assert events == ['changed'] * 2

    # next 3 times, too long
    PAYLOAD_KEYWORD = 'Payload size exceeds the maximum allowed limit.'
    messages = [log['message'] for log in screen.selenium.get_log('browser') if PAYLOAD_KEYWORD in log['message']]
    assert len(messages) == 3

    # check for increasing lengths
    lengths = [int(msg.rpartition(' ')[-1]) for msg in messages]
    for i, j in zip(lengths, lengths[1:]):
        assert i + 1 == j
