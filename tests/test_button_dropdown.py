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


def test_auto_close(screen: Screen):
    with ui.dropdown_button('Button 1', auto_close=False):
        ui.label('Item 1')
    with ui.dropdown_button('Button 2', auto_close=True):
        ui.label('Item 2')

    screen.open('/')
    screen.click('Button 1')
    screen.click('Item 1')
    screen.wait(0.5)
    screen.should_contain('Item 1')

    screen.click('Button 2')
    screen.click('Item 2')
    screen.wait(0.5)
    screen.should_not_contain('Item 2')
