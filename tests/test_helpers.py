import contextlib
import socket
import time
import webbrowser
from pathlib import Path

from nicegui import helpers

TEST_DIR = Path(__file__).parent


def test_is_port_open():
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(('127.0.0.1', 0))  # port = 0 => the OS chooses a port for us
        sock.listen(1)
        host, port = sock.getsockname()
    assert not helpers.is_port_open(host, port), 'after closing the socket, the port should be free'

    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(('127.0.0.1', port))
        sock.listen(1)
        assert helpers.is_port_open(host, port), 'after opening the socket, the port should be detected'


def test_is_port_open_on_bad_ip():
    assert not helpers.is_port_open('1.2', 0), 'should not be able to connect to a bad IP'


def test_schedule_browser(monkeypatch):
    called_with_url = None

    def mock_webbrowser_open(url):
        nonlocal called_with_url
        called_with_url = url

    monkeypatch.setattr(webbrowser, 'open', mock_webbrowser_open)

    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(('127.0.0.1', 0))
        host, port = sock.getsockname()

        _, cancel_event = helpers.schedule_browser(host, port)

        try:
            # port bound, but not opened yet
            assert called_with_url is None

            sock.listen()
            # port opened
            time.sleep(1)
            assert called_with_url == f'http://{host}:{port}/'
        finally:
            cancel_event.set()


def test_canceling_schedule_browser(monkeypatch):
    called_with_url = None

    def mock_webbrowser_open(url):
        nonlocal called_with_url
        called_with_url = url

    monkeypatch.setattr(webbrowser, 'open', mock_webbrowser_open)

    # find a free port ...
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    host, port = sock.getsockname()
    # ... and close it so schedule_browser does not launch the browser
    sock.close()

    thread, cancel_event = helpers.schedule_browser(host, port)
    time.sleep(0.2)
    cancel_event.set()
    time.sleep(0.2)
    assert not thread.is_alive()
    assert called_with_url is None


def test_is_file():
    assert helpers.is_file(TEST_DIR / 'test_helpers.py')
    assert helpers.is_file(str(TEST_DIR / 'test_helpers.py'))
    assert not helpers.is_file(TEST_DIR / 'nonexistent_file')
    assert not helpers.is_file(str(TEST_DIR / 'nonexistent_file'))
    assert not helpers.is_file('data:image/png;base64,...')
    assert not helpers.is_file(None)
    assert not helpers.is_file('x' * 100_000), 'a very long filepath should not lead to OSError 63'
    assert not helpers.is_file('https://nicegui.io/logo.png')


def test_event_type_to_camel_case():
    assert helpers.event_type_to_camel_case('click') == 'click'
    assert helpers.event_type_to_camel_case('row-click') == 'rowClick'
    assert helpers.event_type_to_camel_case('update:model-value') == 'update:modelValue'
    assert helpers.event_type_to_camel_case('keydown.enter') == 'keydown.enter'
    assert helpers.event_type_to_camel_case('keydown.+') == 'keydown.+'
    assert helpers.event_type_to_camel_case('keydown.-') == 'keydown.-'
