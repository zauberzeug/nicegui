from nicegui import ui
from nicegui.testing import Screen


def test_code(screen: Screen):
    @ui.page('/')
    def page():
        ui.code('x = 42')

    screen.open('/')
    assert screen.find_by_class('n').text == 'x'
    assert screen.find_by_class('o').text == '='
    assert screen.find_by_class('mi').text == '42'
