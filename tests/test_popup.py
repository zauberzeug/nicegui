from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from nicegui import ui
from nicegui.testing import Screen


def test_popup(screen: Screen):
    data = {'name': 'Alice'}
    popups: list[ui.popup] = []

    @ui.page('/')
    def page():
        with ui.label().bind_text_from(data, 'name'):
            with ui.popup() as popup:
                ui.input('Name').bind_value(data, 'name')
        popups.append(popup)

    screen.open('/')
    screen.should_contain('Alice')

    screen.click('Alice')  # click the anchor label to open the popup
    screen.wait_for(lambda: popups[0].value)

    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Name"]')
    element.send_keys(' Smith')  # editing the child input updates the bound data...
    screen.wait_for(lambda: data['name'] == 'Alice Smith')
    screen.should_contain('Alice Smith')  # ...and the bound label reflects it live

    element.send_keys(Keys.ESCAPE)
    screen.wait_for(lambda: not popups[0].value)
    assert data['name'] == 'Alice Smith'

    screen.click('Alice Smith')  # re-open: the input still reflects the current value (regression test for #2149)
    screen.should_contain_input('Alice Smith')

    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Name"]')
    element.send_keys(Keys.ESCAPE)
    screen.wait_for(lambda: not popups[0].value)

    popups[0].open()  # programmatic open/close from the server
    screen.should_contain_input('Alice Smith')
    popups[0].close()
    screen.wait_for(lambda: not screen.selenium.find_elements(By.XPATH, '//*[@aria-label="Name"]'))
