from nicegui import ui
from nicegui.testing import SharedScreen


def test_button_group(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.button_group():
            ui.button('Button 1', on_click=lambda: ui.label('Button 1 clicked'))
            ui.button('Button 2', on_click=lambda: ui.label('Button 2 clicked'))
            with ui.dropdown_button('Button 3', on_click=lambda: ui.label('Button 3 clicked')):
                ui.item('Item', on_click=lambda: ui.label('Item clicked'))

    shared_screen.open('/')
    shared_screen.click('Button 1')
    shared_screen.should_contain('Button 1 clicked')

    shared_screen.click('Button 2')
    shared_screen.should_contain('Button 2 clicked')

    shared_screen.click('Button 3')
    shared_screen.should_contain('Button 3 clicked')

    shared_screen.click('Item')
    shared_screen.should_contain('Item clicked')
