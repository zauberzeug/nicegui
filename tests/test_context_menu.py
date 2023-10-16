from nicegui import ui

from .screen import Screen


def test_context_menu(screen: Screen):
    with ui.label('Right-click me'):
        with ui.context_menu():
            ui.menu_item('Item 1')
            ui.menu_item('Item 2')

    screen.open('/')
    screen.context_click('Right-click me')
    screen.should_contain('Item 1')
