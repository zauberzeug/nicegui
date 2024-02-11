from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_clicking_items(screen: SeleniumScreen):
    with ui.list():
        with ui.item(on_click=lambda: ui.notify('Clicked item 1')):
            with ui.item_section():
                ui.item_label('Item 1')
        with ui.item(on_click=lambda: ui.notify('Clicked item 2')):
            with ui.item_section():
                ui.item_label('Item 2')
            with ui.item_section():
                ui.button('Button').on('click.stop', lambda: ui.notify('Clicked button!'))

    screen.open('/')
    screen.click('Item 1')
    screen.should_contain('Clicked item 1')

    screen.click('Item 2')
    screen.should_contain('Clicked item 2')

    screen.click('Button')
    screen.should_contain('Clicked button!')
