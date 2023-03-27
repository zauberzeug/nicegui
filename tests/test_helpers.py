import contextlib
import socket
import time
import webbrowser

from nicegui import helpers


def test_is_port_open():
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:

        sock.bind(('127.0.0.1', 0))  # port = 0 => the OS chooses a port for us
        host, port = sock.getsockname()

        # port bound, but not opened yet
        assert not helpers.is_port_open(host, port)

        sock.listen()
        # port opened
        assert helpers.is_port_open(host, port)


def test_schedule_browser(monkeypatch):

    called_with_url = None

    def mock_webbrowser_open(url):
        nonlocal called_with_url
        called_with_url = url

    monkeypatch.setattr(webbrowser, "open", mock_webbrowser_open)

    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:

        sock.bind(('127.0.0.1', 0))
        host, port = sock.getsockname()

        thread, cancel_event = helpers.schedule_browser(host, port)

        try:
            # port bound, but not opened yet
            assert called_with_url is None

            sock.listen()
            # port opened
            time.sleep(1)
            assert called_with_url == f"http://{host}:{port}/"
        finally:
            cancel_event.set()


def test_schedule_browser_cancel(monkeypatch):

    called_with_url = None

    def mock_webbrowser_open(url):
        nonlocal called_with_url
        called_with_url = url

    monkeypatch.setattr(webbrowser, "open", mock_webbrowser_open)

    # This test doesn't need to open a port, but it binds a socket, s.th. we can be sure
    # it is NOT open.

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    host, port = sock.getsockname()

    thread, cancel_event = helpers.schedule_browser(host, port)

    cancel_event.set()

    time.sleep(1)

    assert not thread.is_alive()
    assert called_with_url is None
