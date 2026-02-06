from selenium.webdriver.common.keys import Keys

from nicegui import ui
from nicegui.testing import SharedScreen


def test_entering_color(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.color_input(label='Color', on_change=lambda e: ui.label(f'content: {e.value}'), preview=True)

    shared_screen.open('/')
    shared_screen.type(Keys.TAB)
    shared_screen.type('#001100')
    shared_screen.should_contain('content: #001100')
    button = shared_screen.find_by_class('q-btn')
    assert button.value_of_css_property('background-color') == 'rgba(0, 17, 0, 1)'


def test_picking_color(shared_screen: SharedScreen):
    output = None

    @ui.page('/')
    def page():
        nonlocal output
        ui.color_input(label='Color', on_change=lambda e: output.set_text(e.value))
        output = ui.label()

    shared_screen.open('/')
    shared_screen.click('colorize')
    shared_screen.click_at_position(shared_screen.find('HEX'), x=0, y=60)
    content = shared_screen.find_by_class('q-color-picker__header-content')
    assert content.value_of_css_property('background-color') in {'rgba(245, 186, 186, 1)', 'rgba(245, 184, 184, 1)'}
    assert output.text in {'#f5baba', '#f5b8b8'}

    shared_screen.type(Keys.ESCAPE)
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('HEX')

    shared_screen.click('colorize')
    content = shared_screen.find_by_class('q-color-picker__header-content')
    assert content.value_of_css_property('background-color') in {'rgba(245, 186, 186, 1)', 'rgba(245, 184, 184, 1)'}
    assert output.text in {'#f5baba', '#f5b8b8'}
