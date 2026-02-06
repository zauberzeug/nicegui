from nicegui import ui
from nicegui.testing import SharedScreen


def test_menu(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.button('Menu'):
            with ui.menu():
                ui.menu_item('Item 1')
                ui.menu_item('Item 2')
                ui.menu_item('Item 3')

    shared_screen.open('/')
    shared_screen.click('Menu')
    shared_screen.should_contain('Item 1')
