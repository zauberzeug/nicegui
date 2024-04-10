from nicegui import ui
from nicegui.testing import Screen


def test_menu(screen: Screen):
    with ui.button('Menu'):
        with ui.menu():
            ui.menu_item('Item 1')
            ui.menu_item('Item 2')
            ui.menu_item('Item 3')

    screen.open('/')
    screen.click('Menu')
    screen.should_contain('Item 1')
