from nicegui import ui
from nicegui.testing import Screen


def test_dropdown_button(screen: Screen):
    clicks = []
    with ui.dropdown_button('Test'):
        with ui.list():
            with ui.item(on_click=lambda: clicks.append(1)):
                ui.item_label('Add 1')
            with ui.item(on_click=lambda: clicks.append(2)):
                ui.item_label('Add 2')

    screen.open('/')
    screen.click('Test')
    screen.should_contain('Add 1')
    screen.click('Add 1')
    screen.wait(0.1)  # NOTE: without auto-close we need to wait here
    assert clicks == [1]
    screen.click('Add 2')
    screen.wait(0.1)
    assert clicks == [1, 2]
