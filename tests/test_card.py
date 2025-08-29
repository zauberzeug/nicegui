from nicegui import ui
from nicegui.testing import Screen


def test_preserve_borders(screen: Screen):
    a = b = None

    @ui.page('/')
    def page():
        nonlocal a, b
        with ui.card():
            a = ui.table(rows=[]).props('bordered flat')
        with ui.card().tight():
            b = ui.table(rows=[]).props('bordered flat')

    screen.open('/')
    assert screen.find_element(a).value_of_css_property('border') == '1px solid rgba(0, 0, 0, 0.12)'
    assert screen.find_element(b).value_of_css_property('border') == '0px none rgb(0, 0, 0)'
