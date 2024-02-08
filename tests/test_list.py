from nicegui import ui
from nicegui.testing import Screen


def test_list(screen: Screen):
    with ui.button('List'):
        with ui.list():
            with ui.item():
                ui.item_label('Test')

    screen.open('/')
    screen.click('List')
    screen.should_contain('Test')


def test_clicking_items(screen: Screen):
    label = ui.label()
    with ui.list():
        with ui.item(on_click=lambda: label.set_text('Clicked item 1')):
            ui.item_label('Item 1')
        with ui.item(on_click=lambda: label.set_text('Clicked item 2')):
            ui.item_label('Item 2')

    screen.open('/')
    screen.should_contain('Item 1')
    screen.should_contain('Item 2')

    screen.click('Item 1')
    screen.should_contain('Clicked item 1')


def test_clicking_nested_sections(screen: Screen):
    label = ui.label()
    with ui.list():
        with ui.item(on_click=lambda: label.set_text('Clicked!')):
            with ui.item_section().props('avatar'):
                ui.button('Button').on('click.stop', lambda: label.set_text('Clicked button!'))
            with ui.item_section():
                ui.item_label('Item')

    screen.open('/')
    screen.should_contain('Button')
    screen.should_contain('Item')

    screen.click('Button')
    screen.should_contain('Clicked button!')

    screen.click('Item')
    screen.should_contain('Clicked!')
