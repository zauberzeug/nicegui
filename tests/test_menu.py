from nicegui import ui

from .screen import Screen


def test_menu(screen: Screen):
    with ui.button('Menu'):
        with ui.menu():
            ui.menu_item('Item 1')
            ui.menu_item('Item 2')
            ui.menu_item('Item 3')

    screen.open('/')
    screen.click('Menu')
    screen.should_contain('Item 1')


def test_context_menu(screen: Screen):
    with ui.label('Right-click me'):
        with ui.context_menu():
            ui.menu_item('Item 1')
            ui.menu_item('Item 2')

    screen.open('/')
    screen.context_click('Right-click me')
    screen.should_contain('Item 1')
