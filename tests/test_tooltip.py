import pytest
from selenium.webdriver import ActionChains

from nicegui import ui
from nicegui.testing import SharedScreen


@pytest.mark.parametrize('element', [ui.label, ui.button, ui.markdown])
def test_tooltip_method(shared_screen: SharedScreen, element: type[ui.element]):
    @ui.page('/')
    def page():
        element('Hover').tooltip('OK')

    shared_screen.open('/')
    ActionChains(shared_screen.selenium).move_to_element(shared_screen.find('Hover')).perform()
    shared_screen.should_contain('OK')
