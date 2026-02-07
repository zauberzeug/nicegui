import pytest

from nicegui import ui
from nicegui.testing import Screen


@pytest.fixture(autouse=True)
def enable_csp_for_module(enable_csp):
    """Enable CSP for all tests in this module to verify CSP compatibility."""
    yield




@pytest.mark.parametrize('add_scroll_padding', [True, False])
def test_no_scroll_padding(screen: Screen, add_scroll_padding: bool):
    @ui.page('/')
    def page():
        ui.header(add_scroll_padding=add_scroll_padding).classes('h-[50px]')
        for i in range(100):
            with ui.link_target(f'line{i}'):
                ui.link(f'Line {i}', f'#line{i}')

    screen.open('/')
    screen.should_contain('Line 0')

    screen.click('Line 10')
    screen.wait(0.5)
    line_y = screen.selenium.execute_script("return arguments[0].getBoundingClientRect()['y'];", screen.find('Line 10'))
    if add_scroll_padding:
        assert line_y > 50
    else:
        assert line_y < 50
