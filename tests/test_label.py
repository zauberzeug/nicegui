from nicegui import ui
from nicegui.testing import Screen


def test_hello_world(screen: Screen):
    ui.label('Hello, world')

    screen.open('/')
    screen.should_contain('Hello, world')


def test_text_0(screen: Screen):
    ui.label(0)

    screen.open('/')
    screen.should_contain('0')
