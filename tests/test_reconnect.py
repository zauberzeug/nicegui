from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import Screen


def test_reconnecting_without_page_reload(screen: Screen):
    @ui.page('/', reconnect_timeout=3.0)
    def page():
        ui.input('Input').props('autofocus')
        ui.button('drop connection', on_click=lambda: ui.run_javascript('socket.io.engine.close()'))

    screen.open('/')
    screen.type('hello')
    screen.click('drop connection')
    screen.wait(2.0)
    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Input"]')
    assert element.get_attribute('value') == 'hello', 'input should be preserved after reconnect (i.e. no page reload)'


def test_reconnecting_after_ack_does_not_reload(screen: Screen):
    @ui.page('/', reconnect_timeout=3.0)
    def page():
        ui.input('Input').props('autofocus')
        label = ui.label('0')
        ui.timer(0.2, lambda: label.set_text(str(int(label.text) + 1)))

    screen.open('/')
    screen.type('hello')
    initial_document_id = screen.selenium.execute_script('return window.documentId;')

    screen.wait(4.0)  # > 3s for the periodic ack to fire and prune message 0 server-side
    assert screen.selenium.execute_script('return Number(window.nextMessageId);') > 0

    screen.selenium.execute_script('window.socket.io.engine.transport.onClose("transport close");')  # drop connection
    screen.wait(4.0)
    assert screen.selenium.execute_script('return window.socket.connected;')
    assert screen.selenium.execute_script('return window.documentId;') == initial_document_id
    assert screen.selenium.find_element(By.XPATH, '//*[@aria-label="Input"]').get_attribute('value') == 'hello'


def test_reconnect_attempt_refreshes_query_next_message_id(screen: Screen):
    @ui.page('/', reconnect_timeout=3.0)
    def page():
        label = ui.label('0')
        ui.timer(0.2, lambda: label.set_text(str(int(label.text) + 1)))

    screen.open('/')
    screen.wait(1.5)
    assert screen.selenium.execute_script('return Number(window.socket.io.opts.query.next_message_id);') == 0
    assert screen.selenium.execute_script('return Number(window.nextMessageId);') > 0

    screen.selenium.execute_script('window.socket.io.engine.transport.onClose("transport close");')
    screen.wait(2.0)
    assert screen.selenium.execute_script('return Number(window.socket.io.opts.query.next_message_id);') > 0
