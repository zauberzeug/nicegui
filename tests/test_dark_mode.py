from typing import Literal

import pytest

from nicegui import app, ui
from nicegui.testing import SharedScreen


@pytest.mark.parametrize('unocss', [None, 'mini', 'wind3', 'wind4'])
def test_dark_mode(shared_screen: SharedScreen, unocss: Literal['mini', 'wind3', 'wind4'] | None):
    app.config.unocss = unocss

    @ui.page('/')
    def page():
        ui.label('Hello')
        dark = ui.dark_mode()
        ui.button('Dark', on_click=dark.enable)
        ui.button('Light', on_click=dark.disable)
        ui.button('Auto', on_click=dark.auto)
        ui.button('Toggle', on_click=dark.toggle)

    def assert_dark(value: bool) -> None:
        classes = (shared_screen.find_by_tag('body').get_attribute('class') or '').split()
        assert ('body--dark' in classes) == value
        assert ('body--light' in classes) != value

    shared_screen.open('/')
    shared_screen.should_contain('Hello')
    assert_dark(False)

    shared_screen.click('Dark')
    shared_screen.wait(0.5)
    assert_dark(True)

    shared_screen.click('Auto')
    shared_screen.wait(0.5)
    assert_dark(False)

    shared_screen.click('Toggle')
    shared_screen.wait(0.5)
    shared_screen.assert_py_logger('ERROR', 'Cannot toggle dark mode when it is set to auto.')

    shared_screen.click('Light')
    shared_screen.wait(0.5)
    assert_dark(False)

    shared_screen.click('Toggle')
    shared_screen.wait(0.5)
    assert_dark(True)
