from nicegui import ui
from nicegui.testing import Screen
import pytest



@pytest.fixture(autouse=True)
def enable_csp_for_module(enable_csp):
    """Enable CSP for all tests in this module to verify CSP compatibility."""
    yield




def test_code(screen: Screen):
    @ui.page('/')
    def page():
        ui.code('x = 42')

    screen.open('/')
    assert screen.find_by_class('n').text == 'x'
    assert screen.find_by_class('o').text == '='
    assert screen.find_by_class('mi').text == '42'
