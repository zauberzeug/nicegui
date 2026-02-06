from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import SharedScreen


def test_spinner(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.spinner(size='3em', thickness=10)

    shared_screen.open('/')
    element = shared_screen.find_by_tag('svg')
    assert element.get_attribute('width') == '3em'
    assert element.get_attribute('height') == '3em'
    assert element.find_element(By.TAG_NAME, 'circle').get_attribute('stroke-width') == '10'
