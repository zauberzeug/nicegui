from nicegui import ui
from nicegui.testing import Screen


def test_menu(screen: Screen):
    ui.codemirror("Line 1\nLine 2\nLine 3"))

    screen.open('/')
    screen.should_contain('Line 1')
