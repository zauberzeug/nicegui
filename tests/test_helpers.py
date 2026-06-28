import contextlib
import functools
import socket
import time
import webbrowser
from inspect import Parameter, Signature
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


def test_is_port_open_on_invalid_endpoint():
    assert not helpers.is_port_open('0.0.0.0', 0), 'should not be able to connect to an invalid endpoint'


def test_format_url():
    assert helpers.format_url('http', 'localhost', 80) == 'http://localhost'  # default port 80 is omitted
    assert helpers.format_url('http', 'localhost', 8080) == 'http://localhost:8080'  # non-default port is included
    assert helpers.format_url('https', 'xyz.com', 443) == 'https://xyz.com'  # default port 443 is omitted
    assert helpers.format_url('https', 'xyz.com', 8443) == 'https://xyz.com:8443'  # non-default port is included
    assert helpers.format_url('http', '::', 8080) == 'http://[::]:8080'  # IPv6 address is enclosed in brackets
    assert helpers.format_url('http', '[::]', 8080) == 'http://[::]:8080'  # already bracketed IPv6 address is unchanged


def test_schedule_browser(monkeypatch):
    opened_urls: list[str] = []
    monkeypatch.setattr(webbrowser, 'open', opened_urls.append)

    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(('127.0.0.1', 0))
        host, port = sock.getsockname()

        _, cancel_event = helpers.schedule_browser('http', host, port, '/my-path')

        try:
            # port bound, but not opened yet
            assert not opened_urls

            sock.listen()
            # port opened
            time.sleep(1)
            assert opened_urls == [f'http://{host}:{port}/my-path']
        finally:
            cancel_event.set()


def test_canceling_schedule_browser(monkeypatch):
    opened_urls: list[str] = []
    monkeypatch.setattr(webbrowser, 'open', opened_urls.append)

    # find a free port ...
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    host, port = sock.getsockname()
    # ... and close it so schedule_browser does not launch the browser
    sock.close()

    thread, cancel_event = helpers.schedule_browser('http', host, port, '/my-path')
    time.sleep(0.2)
    cancel_event.set()
    time.sleep(0.2)
    assert not thread.is_alive()
    assert not opened_urls


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


def test_expects_arguments():
    def no_args():
        pass

    def optional_arg(value=None):
        pass

    def one_arg(value):
        pass

    def var_args(*args, **kwargs):
        pass

    def keyword_only(*, value):
        pass

    class Example:
        def method(self):
            pass

        def method_with_arg(self, value):
            pass

    assert not helpers.expects_arguments(no_args)
    assert not helpers.expects_arguments(optional_arg)
    assert helpers.expects_arguments(one_arg)
    assert not helpers.expects_arguments(var_args)
    assert helpers.expects_arguments(keyword_only)
    assert not helpers.expects_arguments(Example().method)
    assert helpers.expects_arguments(Example().method_with_arg)
    assert not helpers.expects_arguments(functools.partial(one_arg, 1))

    def with_custom_signature():
        pass

    with_custom_signature.__signature__ = Signature([  # type: ignore[attr-defined]
        Parameter('value', Parameter.POSITIONAL_OR_KEYWORD),
    ])
    assert helpers.expects_arguments(with_custom_signature)
