from typing import Literal

import pytest

from nicegui import core, ui
from nicegui.testing import Screen

MAX_SOCKETIO_MESSAGE_SIZE = 1_000_000 - 100


@pytest.mark.parametrize('transport', ['websocket', 'polling'])
def test_socketio_too_long(screen: Screen, transport: Literal['websocket', 'polling']):
    events: list[str] = []
    core.app.config.socket_io_js_transports = [transport]

    @ui.page('/')
    def page():
        ui.textarea(on_change=lambda: events.append('changed'))

    screen.open('/')
    screen.selenium.execute_script('''
        window.__niceguiPayloadLengths = [];
        const transport = window.socket.io.engine.transport;
        const wrap = originalFunction => function (...args) {
            const msg = args[0];
            if (typeof msg === 'string' && msg.includes('["event"')) {
                window.__niceguiPayloadLengths.push(msg.length);
            }
            return originalFunction.call(this, ...args);
        };
        if (transport?.ws?.send) transport.ws.send = wrap(transport.ws.send);
        if (transport?.doWrite) transport.doWrite = wrap(transport.doWrite);
    ''')

    textarea = screen.find_by_tag('textarea')
    textarea.click()
    screen.type('z')
    event_payload_length = screen.selenium.execute_script('return window.__niceguiPayloadLengths.at(-1);')
    payload_overhead = event_payload_length - 1
    initial_value_length = MAX_SOCKETIO_MESSAGE_SIZE - payload_overhead - 2
    events.clear()

    screen.selenium.execute_script('''
        const textarea = document.querySelector('textarea');
        textarea.value = 'x'.repeat(arguments[0]);
        textarea.focus();
        textarea.setSelectionRange(textarea.value.length, textarea.value.length);
        window.__niceguiPayloadLengths = [];
    ''', initial_value_length)
    for _ in range(5):
        screen.type('y')

    assert events == ['changed'] * 2, 'two more characters are ok'
    assert len([log for log in screen.selenium.get_log('browser') if 'Payload size' in log['message']]) == 3
    screen.assert_py_logger('ERROR', f'Payload size {MAX_SOCKETIO_MESSAGE_SIZE + 1} exceeds the maximum allowed limit.')
    screen.assert_py_logger('ERROR', f'Payload size {MAX_SOCKETIO_MESSAGE_SIZE + 2} exceeds the maximum allowed limit.')
    screen.assert_py_logger('ERROR', f'Payload size {MAX_SOCKETIO_MESSAGE_SIZE + 3} exceeds the maximum allowed limit.')
