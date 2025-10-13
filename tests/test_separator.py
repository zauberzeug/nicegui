from nicegui import ui
from nicegui.testing import Screen


def test_separator(screen: Screen):
    @ui.page('/column')
    def index():
        with ui.column():
            ui.button('1')
            ui.separator()
            ui.button('2')
    @ui.page('/row')
    def index():
        with ui.row():
            ui.button('1')
            ui.separator().props('vertical')
            ui.button('2')


    screen.open('/column')
    assert screen.find_by_tag('hr').value_of_css_property('width') == '100%'

    screen.wait(0.5)
    screen.open('/row')
    assert screen.find_by_tag('hr').value_of_css_property('width') == '1px'
