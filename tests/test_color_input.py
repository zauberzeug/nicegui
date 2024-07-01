from selenium.webdriver.common.keys import Keys

from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_entering_color(screen: SeleniumScreen):
    ui.color_input(label='Color', on_change=lambda e: ui.label(f'content: {e.value}'), preview=True)

    screen.open('/')
    screen.type(Keys.TAB)
    screen.type('#001100')
    screen.should_contain('content: #001100')
    button = screen.find_by_class('q-btn')
    assert button.value_of_css_property('background-color') == 'rgba(0, 17, 0, 1)'


def test_picking_color(screen: SeleniumScreen):
    ui.color_input(label='Color', on_change=lambda e: output.set_text(e.value))
    output = ui.label()

    screen.open('/')
    screen.click('colorize')
    screen.click_at_position(screen.find('HEX'), x=0, y=60)
    content = screen.find_by_class('q-color-picker__header-content')
    assert content.value_of_css_property('background-color') in {'rgba(245, 186, 186, 1)', 'rgba(245, 184, 184, 1)'}
    assert output.text in {'#f5baba', '#f5b8b8'}

    screen.type(Keys.ESCAPE)
    screen.wait(0.5)
    screen.should_not_contain('HEX')

    screen.click('colorize')
    content = screen.find_by_class('q-color-picker__header-content')
    assert content.value_of_css_property('background-color') in {'rgba(245, 186, 186, 1)', 'rgba(245, 184, 184, 1)'}
    assert output.text in {'#f5baba', '#f5b8b8'}
