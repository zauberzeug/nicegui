from nicegui import ui
from nicegui.testing import Screen


def test_dropdown_button(screen: Screen):
    with ui.dropdown_button('Button', on_click=lambda: ui.label('Button clicked')):
        with ui.list():
            with ui.item(on_click=lambda: ui.label('Item clicked')):
                ui.item_label('Item')

    screen.open('/')
    screen.click('Button')
    screen.should_contain('Button clicked')
    screen.click('Item')
    screen.should_contain('Item clicked')
