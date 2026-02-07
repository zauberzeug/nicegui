from nicegui import ui
from nicegui.testing import Screen
import pytest



@pytest.fixture(autouse=True)
def enable_csp_for_module(enable_csp):
    """Enable CSP for all tests in this module to verify CSP compatibility."""
    yield




def test_clicking_items(screen: Screen):
    @ui.page('/')
    def page():
        with ui.list():
            ui.item('Item 1', on_click=lambda: ui.notify('Clicked item 1'))
            with ui.item('Item 2', on_click=lambda: ui.notify('Clicked item 2')):
                with ui.item_section():
                    ui.button('Button').on('click.stop', lambda: ui.notify('Clicked button!'))

    screen.open('/')
    screen.click('Item 1')
    screen.should_contain('Clicked item 1')

    screen.click('Item 2')
    screen.should_contain('Clicked item 2')

    screen.click('Button')
    screen.should_contain('Clicked button!')
