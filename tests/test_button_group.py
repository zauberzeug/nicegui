from nicegui import ui
from nicegui.testing import Screen


def test_group_with_buttons(screen: Screen):
    with ui.button_group():
        ui.button('Button 1')
        ui.button('Button 2')
        ui.button('Button 3')

    screen.open('/')
    screen.should_contain('Button 1')
    screen.should_contain('Button 2')
    screen.should_contain('Button 3')


def test_group_with_dropdown(screen: Screen):
    clicks = []
    with ui.button_group():
        ui.button('Button 1')
        ui.button('Button 2')
        with ui.dropdown_button('Dropdown').props('auto-close'):
            with ui.list():
                with ui.item(on_click=lambda: clicks.append(1)):
                    ui.item_label('Add 1')
                with ui.item(on_click=lambda: clicks.append(2)):
                    ui.item_label('Add 2')

    screen.open('/')
    screen.click('Dropdown')
    screen.click('Add 1')
    assert clicks == [1]
    screen.click('Dropdown')
    screen.click('Add 2')
    assert clicks == [1, 2]
