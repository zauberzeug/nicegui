from nicegui import ui
from nicegui.testing import SharedScreen


def test_hello_world(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.label('Hello, world')

    shared_screen.open('/')
    shared_screen.should_contain('Hello, world')


def test_text_0(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.label(0)

    shared_screen.open('/')
    shared_screen.should_contain('0')
