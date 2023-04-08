from nicegui import ui

from .screen import Screen


def test_quasar_colors(screen: Screen):
    b1 = ui.button()
    b2 = ui.button(color=None)
    b3 = ui.button(color='red-5')
    b4 = ui.button(color='red-500')
    b5 = ui.button(color='#ff0000')

    screen.open('/')
    assert screen.find_by_id(b1.id).value_of_css_property('background-color') == 'rgba(88, 152, 212, 1)'
    assert screen.find_by_id(b2.id).value_of_css_property('background-color') == 'rgba(0, 0, 0, 0)'
    assert screen.find_by_id(b3.id).value_of_css_property('background-color') == 'rgba(239, 83, 80, 1)'
    assert screen.find_by_id(b4.id).value_of_css_property('background-color') == 'rgba(239, 68, 68, 1)'
    assert screen.find_by_id(b5.id).value_of_css_property('background-color') == 'rgba(255, 0, 0, 1)'
