from nicegui import ui
from nicegui.testing import Screen


def test_button_group(screen: Screen):
    with ui.button_group():
        ui.button('Button 1', on_click=lambda: ui.label('Button 1 clicked'))
        ui.button('Button 2', on_click=lambda: ui.label('Button 2 clicked'))
        with ui.dropdown_button('Button 3', on_click=lambda: ui.label('Button 3 clicked')):
            with ui.list():
                with ui.item(on_click=lambda: ui.label('Item clicked')):
                    ui.item_label('Item')

    screen.open('/')
    screen.click('Button 1')
    screen.should_contain('Button 1 clicked')
    screen.click('Button 2')
    screen.should_contain('Button 2 clicked')
    screen.click('Button 3')
    screen.should_contain('Button 3 clicked')
    screen.click('Item')
    screen.should_contain('Item clicked')
