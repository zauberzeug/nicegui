from nicegui import ui
from nicegui.testing import Screen


def test_context_menu(screen: Screen):
    with ui.label('Right-click me'):
        with ui.context_menu():
            ui.menu_item('Item 1', on_click=lambda: ui.notify('You clicked'))
            ui.menu_item('Item 2')

    screen.open('/')
    screen.context_click('Right-click me')
    screen.click('Item 1')
    screen.should_contain('You clicked')
    screen.wait(0.5)
    screen.should_not_contain('Item 1')
