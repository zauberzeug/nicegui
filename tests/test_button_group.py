from nicegui import ui
from nicegui.testing import Screen
import pytest



@pytest.fixture(autouse=True)
def enable_csp_for_module(enable_csp):
    """Enable CSP for all tests in this module to verify CSP compatibility."""
    yield




def test_button_group(screen: Screen):
    @ui.page('/')
    def page():
        with ui.button_group():
            ui.button('Button 1', on_click=lambda: ui.label('Button 1 clicked'))
            ui.button('Button 2', on_click=lambda: ui.label('Button 2 clicked'))
            with ui.dropdown_button('Button 3', on_click=lambda: ui.label('Button 3 clicked')):
                ui.item('Item', on_click=lambda: ui.label('Item clicked'))

    screen.open('/')
    screen.click('Button 1')
    screen.should_contain('Button 1 clicked')

    screen.click('Button 2')
    screen.should_contain('Button 2 clicked')

    screen.click('Button 3')
    screen.should_contain('Button 3 clicked')

    screen.click('Item')
    screen.should_contain('Item clicked')
