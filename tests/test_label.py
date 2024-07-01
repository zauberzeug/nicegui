from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_hello_world(screen: SeleniumScreen):
    ui.label('Hello, world')

    screen.open('/')
    screen.should_contain('Hello, world')


def test_text_0(screen: SeleniumScreen):
    ui.label(0)

    screen.open('/')
    screen.should_contain('0')
