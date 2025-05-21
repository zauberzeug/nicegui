from nicegui import ui
from nicegui.testing import Screen


def test_preserve_borders(screen: Screen):
    with ui.card():
        ui.label('A').classes('border shadow')
    with ui.card().tight():
        ui.label('B').classes('border shadow')

    screen.open('/')
    assert screen.find('A').value_of_css_property('border') == '1px solid rgb(229, 231, 235)'
    assert screen.find('B').value_of_css_property('border') == '0px none rgb(0, 0, 0)'
