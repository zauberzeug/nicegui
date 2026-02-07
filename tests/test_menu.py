from nicegui import ui
from nicegui.testing import Screen
import pytest



@pytest.fixture(autouse=True)
def enable_csp_for_module(enable_csp):
    """Enable CSP for all tests in this module to verify CSP compatibility."""
    yield




def test_menu(screen: Screen):
    @ui.page('/')
    def page():
        with ui.button('Menu'):
            with ui.menu():
                ui.menu_item('Item 1')
                ui.menu_item('Item 2')
                ui.menu_item('Item 3')

    screen.open('/')
    screen.click('Menu')
    screen.should_contain('Item 1')
