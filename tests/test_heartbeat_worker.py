import time

from selenium.webdriver.common.by import By

from nicegui import Client, ui
from nicegui.testing import Screen


def test_connection_survives_alert_dialog(screen: Screen):
    @ui.page('/', reconnect_timeout=3.0)
    def page():
        ui.input('Input').props('autofocus')

    screen.open('/')
    screen.type('hello')

    client_id = screen.selenium.execute_script('return window.clientId')

    screen.selenium.execute_script('setTimeout(() => alert("blocking"), 100)')
    time.sleep(3.5)

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
    time.sleep(3.5)

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
    screen.wait(3.0)

    assert client_id not in Client.instances
