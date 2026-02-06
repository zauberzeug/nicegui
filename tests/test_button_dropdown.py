from nicegui import ui
from nicegui.testing import SharedScreen


def test_dropdown_button(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.dropdown_button('Button', on_click=lambda: ui.label('Button clicked')):
            ui.item('Item', on_click=lambda: ui.label('Item clicked'))

    shared_screen.open('/')
    shared_screen.click('Button')
    shared_screen.should_contain('Button clicked')

    shared_screen.click('Item')
    shared_screen.should_contain('Item clicked')


def test_auto_close(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.dropdown_button('Button 1', auto_close=False):
            ui.label('Item 1')
        with ui.dropdown_button('Button 2', auto_close=True):
            ui.label('Item 2')

    shared_screen.open('/')
    shared_screen.click('Button 1')
    shared_screen.click('Item 1')
    shared_screen.wait(0.5)
    shared_screen.should_contain('Item 1')

    shared_screen.click('Button 2')
    shared_screen.click('Item 2')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('Item 2')
