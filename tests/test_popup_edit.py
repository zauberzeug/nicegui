from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from nicegui import ui
from nicegui.testing import Screen


def test_popup_edit(screen: Screen):
    events: list[str] = []
    data = {'name': 'Alice'}

    @ui.page('/')
    def page():
        with ui.label().bind_text_from(data, 'name'):
            with ui.popup_edit(on_show=lambda _: events.append('show'),
                               on_hide=lambda _: events.append('hide')):
                ui.input('Name').bind_value(data, 'name')

    screen.open('/')
    screen.should_contain('Alice')

    screen.click('Alice')  # click the anchor label to open the popup
    screen.wait(0.5)
    assert 'show' in events

    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Name"]')
    element.send_keys(' Smith')  # editing the child input updates the bound data...
    screen.wait(0.5)
    assert data['name'] == 'Alice Smith'
    screen.should_contain('Alice Smith')  # ...and the bound label reflects it live

    element.send_keys(Keys.ESCAPE)  # QPopupEdit's cancel does NOT revert, since we do not use its model value
    screen.wait(0.5)
    assert 'hide' in events
    assert data['name'] == 'Alice Smith'

    screen.click('Alice Smith')  # re-open: the input still reflects the current value (regression test for #2149)
    screen.wait(0.5)
    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Name"]')
    assert element.get_attribute('value') == 'Alice Smith'
