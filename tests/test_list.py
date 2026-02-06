from nicegui import ui
from nicegui.testing import SharedScreen


def test_clicking_items(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.list():
            ui.item('Item 1', on_click=lambda: ui.notify('Clicked item 1'))
            with ui.item('Item 2', on_click=lambda: ui.notify('Clicked item 2')):
                with ui.item_section():
                    ui.button('Button').on('click.stop', lambda: ui.notify('Clicked button!'))

    shared_screen.open('/')
    shared_screen.click('Item 1')
    shared_screen.should_contain('Clicked item 1')

    shared_screen.click('Item 2')
    shared_screen.should_contain('Clicked item 2')

    shared_screen.click('Button')
    shared_screen.should_contain('Clicked button!')
