from nicegui import ui
from nicegui.testing import Screen
import pytest



@pytest.fixture(autouse=True)
def enable_csp_for_module(enable_csp):
    """Enable CSP for all tests in this module to verify CSP compatibility."""
    yield




def test_knob(screen: Screen):
    @ui.page('/')
    def page():
        knob = ui.knob(0.3, show_value=True)
        ui.button('turn up', on_click=lambda: knob.set_value(0.8))

    screen.open('/')
    screen.should_contain('0.3')
    screen.click('turn up')
    screen.should_contain('0.8')
