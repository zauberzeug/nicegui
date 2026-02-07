from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import Screen
import pytest



@pytest.fixture(autouse=True)
def enable_csp_for_module(enable_csp):
    """Enable CSP for all tests in this module to verify CSP compatibility."""
    yield




def test_spinner(screen: Screen):
    @ui.page('/')
    def page():
        ui.spinner(size='3em', thickness=10)

    screen.open('/')
    element = screen.find_by_tag('svg')
    assert element.get_attribute('width') == '3em'
    assert element.get_attribute('height') == '3em'
    assert element.find_element(By.TAG_NAME, 'circle').get_attribute('stroke-width') == '10'
