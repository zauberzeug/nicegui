import time

from selenium.webdriver.common.by import By

from nicegui import Client, ui
from nicegui.testing import Screen


def test_connection_survives_alert_dialog(screen: Screen):
    """Test that a blocking alert() dialog does not kill the connection."""
    @ui.page('/', reconnect_timeout=3.0)
    def page():
        ui.input('Input').props('autofocus')

    screen.open('/')
    screen.type('hello')

    client_id = screen.selenium.execute_script('return window.clientId')

    # Open a blocking alert dialog (freezes the main JS thread)
    screen.selenium.execute_script('setTimeout(() => alert("blocking"), 100)')
    time.sleep(0.5)
    # Main JS thread is now frozen — Socket.IO cannot respond to pings

    # Wait longer than reconnect_timeout while the dialog is open
    time.sleep(5.0)

    # Client must still exist thanks to heartbeat worker
    assert client_id in Client.instances, 'client should survive blocking dialog thanks to heartbeat'

    # Dismiss the alert — main thread resumes, Socket.IO auto-reconnects
    screen.selenium.switch_to.alert.accept()
    screen.wait(2.0)

    # Input value should be preserved (no page reload happened)
    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Input"]')
    assert element.get_attribute('value') == 'hello', 'input should be preserved after reconnect'


def test_connection_survives_alert_with_high_reconnect_timeout(screen: Screen):
    """Test with reconnect_timeout=10 (like main.py) after many messages have been sent."""
    counter = {'value': 0}

    @ui.page('/', reconnect_timeout=10.0)
    def page():
        label = ui.label('0')
        ui.input('Input').props('autofocus')
        ui.timer(0.05, lambda: label.set_text(str(counter.__setitem__('value', counter['value'] + 1) or counter['value'])))

    screen.open('/')
    screen.type('hello')

    # Let the timer generate many messages so the early message history gets pruned
    screen.wait(3.0)

    client_id = screen.selenium.execute_script('return window.clientId')
    next_msg_id = screen.selenium.execute_script('return window.nextMessageId')
    assert next_msg_id > 10, f'expected many messages, got {next_msg_id}'

    # Block the main thread with alert
    screen.selenium.execute_script('setTimeout(() => alert("blocking"), 100)')
    time.sleep(0.5)
    time.sleep(15.0)  # longer than ping_interval(8) + ping_timeout(4) = 12s

    assert client_id in Client.instances, 'client should survive thanks to heartbeat'

    # Dismiss alert — Socket.IO reconnects with current next_message_id (not stale one)
    screen.selenium.switch_to.alert.accept()
    screen.wait(3.0)

    # Input value should be preserved (no page reload)
    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Input"]')
    assert element.get_attribute('value') == 'hello', 'input should be preserved (no reload)'


def test_heartbeat_worker_is_started(screen: Screen):
    """Test that the heartbeat worker is created on page load."""
    @ui.page('/')
    def page():
        ui.label('Hello')

    screen.open('/')
    has_worker = screen.selenium.execute_script('return window.heartbeatWorker !== undefined')
    assert has_worker, 'heartbeat worker should be created'


def test_client_deleted_when_heartbeat_stops(screen: Screen):
    """Test that the client is eventually deleted when browser navigates away (worker stops)."""
    @ui.page('/', reconnect_timeout=1.0)
    def page():
        ui.label('Hello')

    screen.open('/')
    client_id = screen.selenium.execute_script('return window.clientId')
    assert client_id in Client.instances

    # Navigate away (this stops the worker and socket)
    screen.selenium.get('about:blank')
    screen.wait(3.0)

    # Client should be deleted since no heartbeat is being sent
    assert client_id not in Client.instances, 'client should be deleted after navigation away'
