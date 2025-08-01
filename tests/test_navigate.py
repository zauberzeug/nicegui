import pytest

from nicegui import ui
from nicegui.testing import Screen


@pytest.mark.parametrize('new_tab', [False, True])
def test_navigate_to(screen: Screen, new_tab: bool):
    @ui.page('/test_page')
    def page():
        ui.label('Test page')
        ui.button('Back', on_click=ui.navigate.back)
    ui.button('Open test page', on_click=lambda: ui.navigate.to('/test_page', new_tab=new_tab))
    ui.button('Forward', on_click=ui.navigate.forward)

    screen.open('/')
    screen.click('Open test page')
    screen.wait(0.5)
    screen.switch_to(1 if new_tab else 0)
    screen.should_contain('Test page')

    if not new_tab:
        screen.click('Back')
        screen.should_contain('Open test page')

        screen.click('Forward')
        screen.should_contain('Test page')


def test_navigate_to_absolute_url(screen: Screen):
    external_url = 'https://nicegui.io'
    ui.button('Go external', on_click=lambda: ui.navigate.to(external_url))

    screen.open('/')
    screen.click('Go external')
    screen.wait(1.0)
    # After clicking, the page should navigate away from NiceGUI app.
    # We can check that the URL is now external, or alternatively that NiceGUI UI is gone.
    assert external_url in screen.selenium.current_url
