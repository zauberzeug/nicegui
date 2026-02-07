import pytest
from selenium.webdriver import ActionChains

from nicegui import ui
from nicegui.testing.screen import Screen


@pytest.fixture(autouse=True)
def enable_csp_for_module(enable_csp):
    """Enable CSP for all tests in this module to verify CSP compatibility."""
    yield




@pytest.mark.parametrize('element', [ui.label, ui.button, ui.markdown])
def test_tooltip_method(screen: Screen, element: type[ui.element]):
    @ui.page('/')
    def page():
        element('Hover').tooltip('OK')

    screen.open('/')
    ActionChains(screen.selenium).move_to_element(screen.find('Hover')).perform()
    screen.should_contain('OK')
