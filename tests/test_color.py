from nicegui import color, ui
from nicegui.testing import Screen


def test_color_constants(screen: Screen):
    icon1 = ui.icon('home', color=color.RED)
    icon2 = ui.icon('home', color=color.quasar.RED_5)
    icon3 = ui.icon('home', color=color.tailwind.RED_500)

    screen.open('/')
    assert screen.find_element(icon1).value_of_css_property('color') == 'rgba(244, 67, 54, 1)'
    assert screen.find_element(icon2).value_of_css_property('color') == 'rgba(239, 83, 80, 1)'
    assert screen.find_element(icon3).value_of_css_property('color') == 'rgba(239, 68, 68, 1)'
