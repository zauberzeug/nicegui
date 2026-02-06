from nicegui import ui
from nicegui.testing import SharedScreen


def test_teleport(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.card().classes('card')

        def create_teleport():
            with ui.teleport('.card'):
                ui.label('Hello')

        ui.button('create', on_click=create_teleport)

    shared_screen.open('/')
    shared_screen.click('create')
    assert shared_screen.find_by_css('.card > div').text == 'Hello'


def test_teleport_with_element(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        card = ui.card().classes('card')

        def create_teleport():
            with ui.teleport(card):
                ui.label('Hello')

        ui.button('create', on_click=create_teleport)

    shared_screen.open('/')
    shared_screen.click('create')
    assert shared_screen.find_by_css('.card > div').text == 'Hello'


def test_update(shared_screen: SharedScreen):
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

    shared_screen.open('/')
    shared_screen.click('create')
    shared_screen.should_contain('Hello')
    shared_screen.click('rebuild card')
    shared_screen.should_contain('Card rebuilt')
    assert shared_screen.find_by_css('.card > div').text == 'Hello'
