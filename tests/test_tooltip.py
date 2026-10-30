from collections.abc import Callable

import pytest
from selenium.webdriver import ActionChains

from nicegui import ui
from nicegui.testing.screen import Screen


@pytest.mark.parametrize('element', [
    ui.label,
    ui.button,
    ui.markdown,
    lambda text: ui.select(['A'], label=text).classes('w-40'),
    lambda text: ui.select(['A'], label=text, with_input=True).classes('w-40'),
])
def test_tooltip_method(screen: Screen, element: Callable[[str], ui.element]):
    @ui.page('/')
    def page():
        element('Hover').tooltip('OK')

    screen.open('/')
    ActionChains(screen.selenium).move_to_element(screen.find('Hover')).perform()
    screen.should_contain('OK')
