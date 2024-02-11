import pytest

from nicegui import ui
from nicegui.testing import SeleniumScreen


@pytest.mark.parametrize('new_tab', [False, True])
def test_open_page(screen: SeleniumScreen, new_tab: bool):
    @ui.page('/test_page')
    def page():
        ui.label('Test page')
    ui.button('Open test page', on_click=lambda: ui.open('/test_page', new_tab=new_tab))

    screen.open('/')
    screen.click('Open test page')
    screen.wait(0.5)
    screen.switch_to(1 if new_tab else 0)
    screen.should_contain('Test page')
