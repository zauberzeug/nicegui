from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_quasar_colors(screen: SeleniumScreen):
    b1 = ui.button()
    b2 = ui.button(color=None)
    b3 = ui.button(color='red-5')
    b4 = ui.button(color='red-500')
    b5 = ui.button(color='#ff0000')

    screen.open('/')
    assert screen.find_element(b1).value_of_css_property('background-color') == 'rgba(88, 152, 212, 1)'
    assert screen.find_element(b2).value_of_css_property('background-color') == 'rgba(0, 0, 0, 0)'
    assert screen.find_element(b3).value_of_css_property('background-color') == 'rgba(239, 83, 80, 1)'
    assert screen.find_element(b4).value_of_css_property('background-color') == 'rgba(239, 68, 68, 1)'
    assert screen.find_element(b5).value_of_css_property('background-color') == 'rgba(255, 0, 0, 1)'


def test_enable_disable(screen: SeleniumScreen):
    events = []
    b = ui.button('Button', on_click=lambda: events.append(1))
    ui.button('Enable', on_click=b.enable)
    ui.button('Disable', on_click=b.disable)

    screen.open('/')
    screen.click('Button')
    assert events == [1]
    screen.click('Disable')
    screen.click('Button')
    assert events == [1]
    screen.click('Enable')
    screen.click('Button')
    assert events == [1, 1]
