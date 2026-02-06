import pytest

from nicegui import ui
from nicegui.testing import SharedScreen


@pytest.mark.parametrize('add_scroll_padding', [True, False])
def test_no_scroll_padding(shared_screen: SharedScreen, add_scroll_padding: bool):
    @ui.page('/')
    def page():
        ui.header(add_scroll_padding=add_scroll_padding).classes('h-[50px]')
        for i in range(100):
            with ui.link_target(f'line{i}'):
                ui.link(f'Line {i}', f'#line{i}')

    shared_screen.open('/')
    shared_screen.should_contain('Line 0')

    shared_screen.click('Line 10')
    shared_screen.wait(0.5)
    line_y = shared_screen.selenium.execute_script("return arguments[0].getBoundingClientRect()['y'];", shared_screen.find('Line 10'))
    if add_scroll_padding:
        assert line_y > 50
    else:
        assert line_y < 50
