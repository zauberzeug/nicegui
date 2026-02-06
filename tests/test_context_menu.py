from nicegui import ui
from nicegui.testing import SharedScreen


def test_context_menu(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.label('Right-click me'):
            with ui.context_menu():
                ui.item('Menu')
                ui.menu_item('Item 1', auto_close=False)
                ui.menu_item('Item 2', on_click=lambda: ui.notify('You clicked'))

    shared_screen.open('/')
    shared_screen.context_click('Right-click me')
    shared_screen.should_contain('Menu')

    shared_screen.click('Item 1')
    shared_screen.wait(0.5)
    shared_screen.should_contain('Menu')

    shared_screen.click('Item 2')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('Menu')
    shared_screen.should_contain('You clicked')
