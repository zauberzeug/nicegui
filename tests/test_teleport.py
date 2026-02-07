from nicegui import ui
from nicegui.testing import Screen
import pytest



@pytest.fixture(autouse=True)
def enable_csp_for_module(enable_csp):
    """Enable CSP for all tests in this module to verify CSP compatibility."""
    yield




def test_teleport(screen: Screen):
    @ui.page('/')
    def page():
        ui.card().classes('card')

        def create_teleport():
            with ui.teleport('.card'):
                ui.label('Hello')

        ui.button('create', on_click=create_teleport)

    screen.open('/')
    screen.click('create')
    assert screen.find_by_css('.card > div').text == 'Hello'


def test_teleport_with_element(screen: Screen):
    @ui.page('/')
    def page():
        card = ui.card().classes('card')

        def create_teleport():
            with ui.teleport(card):
                ui.label('Hello')

        ui.button('create', on_click=create_teleport)

    screen.open('/')
    screen.click('create')
    assert screen.find_by_css('.card > div').text == 'Hello'


def test_update(screen: Screen):
    @ui.page('/')
    def page():
        teleport: ui.teleport | None = None

        card = ui.card().classes('card')

        def create_teleport():
            nonlocal teleport
            with ui.teleport('.card') as teleport:
                ui.label('Hello')

        ui.button('create', on_click=create_teleport)

        def rebuild_card():
            card.delete()
            ui.card().classes('card')
            assert teleport is not None
            teleport.update()
            ui.notify('Card rebuilt')

        ui.button('rebuild card', on_click=rebuild_card)

    screen.open('/')
    screen.click('create')
    screen.should_contain('Hello')
    screen.click('rebuild card')
    screen.should_contain('Card rebuilt')
    assert screen.find_by_css('.card > div').text == 'Hello'
