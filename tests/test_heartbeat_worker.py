import time

from selenium.webdriver.common.by import By

from nicegui import Client, ui
from nicegui.testing import Screen


def _wait_for_disconnect_to_register(client_id: str, timeout: float = 10) -> None:
    # ping_interval + ping_timeout (>= 6s by default) must elapse before socket.io reports the
    # disconnect server-side; only then does _delete_tasks populate and the heartbeat have work to do.
    deadline = time.time() + timeout
    while time.time() < deadline:
        client = Client.instances.get(client_id)
        if client and client._delete_tasks:  # pylint: disable=protected-access
            return
        time.sleep(0.2)
    raise AssertionError('disconnect was never registered server-side')


def test_connection_survives_alert_dialog(screen: Screen):
    @ui.page('/', reconnect_timeout=3.0)
    def page():
        ui.input('Input').props('autofocus')

    screen.open('/')
    screen.type('hello')

    client_id = screen.selenium.execute_script('return window.clientId')

    screen.selenium.execute_script('setTimeout(() => alert("blocking"), 100)')
    _wait_for_disconnect_to_register(client_id)
    time.sleep(4.0)  # past reconnect_timeout — without the heartbeat the client would be deleted by now

    assert client_id in Client.instances

    screen.selenium.switch_to.alert.accept()
    screen.wait(2.0)

    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Input"]')
    assert element.get_attribute('value') == 'hello'


def test_connection_survives_alert_after_many_messages(screen: Screen):
    counter = [0]

    def increment():
        counter[0] += 1
        return counter[0]

    @ui.page('/', reconnect_timeout=3.0)
    def page():
        label = ui.label('0')
        ui.input('Input').props('autofocus')
        ui.timer(0.02, lambda: label.set_text(str(increment())))

    screen.open('/')
    screen.type('hello')
    screen.wait(1.5)

    client_id = screen.selenium.execute_script('return window.clientId')
    next_msg_id = screen.selenium.execute_script('return window.nextMessageId')
    assert next_msg_id > 10

    screen.selenium.execute_script('setTimeout(() => alert("blocking"), 100)')
    _wait_for_disconnect_to_register(client_id)
    time.sleep(4.0)

    assert client_id in Client.instances

    screen.selenium.switch_to.alert.accept()
    screen.wait(2.0)

    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Input"]')
    assert element.get_attribute('value') == 'hello'


def test_client_deleted_when_heartbeat_stops(screen: Screen):
    @ui.page('/', reconnect_timeout=1.0)
    def page():
        ui.label('Hello')

    screen.open('/')
    client_id = screen.selenium.execute_script('return window.clientId')
    assert client_id in Client.instances

    screen.selenium.get('about:blank')
    screen.wait(8.0)  # > ping_interval + ping_timeout + reconnect_timeout

    assert client_id not in Client.instances
