from selenium.webdriver.common.keys import Keys

from nicegui import ui
from nicegui.testing import Screen


def test_popup(screen: Screen):
    data = {'name': 'Alice'}
    popup = None

    @ui.page('/')
    def page():
        nonlocal popup
        with ui.label().bind_text_from(data, 'name'):
            with ui.popup() as popup:
                ui.input('Name').bind_value(data, 'name')

    screen.open('/')
    screen.click('Alice')  # click the anchor label to open the popup
    screen.wait_for(lambda: popup.value)
    screen.should_contain_input('Alice')  # wait for the popup content to settle

    screen.find_by_tag('input').send_keys(' Smith')  # editing the input updates the bound data...
    screen.wait_for(lambda: data['name'] == 'Alice Smith')
    screen.should_contain('Alice Smith')  # ...and the bound label reflects it live

    screen.find_by_tag('input').send_keys(Keys.ESCAPE)  # close from the client
    screen.wait_for(lambda: not popup.value)
    assert data['name'] == 'Alice Smith'

    screen.click('Alice Smith')  # re-open: the input still shows the current value (regression test for #2149)
    screen.should_contain_input('Alice Smith')

    popup.close()  # close and re-open from the server
    with screen.implicitly_wait(0.1):  # otherwise find_all_by_tag would stall for the full implicit wait once the input is gone
        screen.wait_for(lambda: not screen.find_all_by_tag('input'))
    popup.open()
    screen.should_contain_input('Alice Smith')
