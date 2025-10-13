from nicegui import ui
from nicegui.testing import Screen


def test_context_menu(screen: Screen):
    @ui.page('/')
    def page():
        with ui.label('Right-click me'):
            with ui.context_menu():
                ui.item('Menu')
                ui.menu_item('Item 1', auto_close=False)
                ui.menu_item('Item 2', on_click=lambda: ui.notify('You clicked'))

    screen.open('/')
    screen.context_click('Right-click me')
    screen.should_contain('Menu')

    screen.click('Item 1')
    screen.wait(0.5)
    screen.should_contain('Menu')

    screen.click('Item 2')
    screen.wait(0.5)
    screen.should_not_contain('Menu')
    screen.should_contain('You clicked')
