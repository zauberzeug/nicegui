from nicegui import ui
from nicegui.testing import SharedScreen


def test_code(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.code('x = 42')

    shared_screen.open('/')
    assert shared_screen.find_by_class('n').text == 'x'
    assert shared_screen.find_by_class('o').text == '='
    assert shared_screen.find_by_class('mi').text == '42'
