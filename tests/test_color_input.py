from selenium.webdriver.common.keys import Keys

from nicegui import ui

from .screen import Screen


def test_entering_color(screen: Screen):
    ui.color_input(label='Color', on_change=lambda e: ui.label(f'content: {e.value}'))

    screen.open('/')
    screen.type(Keys.TAB)
    screen.type('#001100')
    screen.should_contain('content: #001100')


def test_picking_color(screen: Screen):
    ui.color_input(label='Color', on_change=lambda e: ui.label(f'content: {e.value}'))

    screen.open('/')
    picker = screen.click('colorize')
    screen.click_at_position(picker, x=40, y=120)
    screen.should_contain('content: #de8383')
