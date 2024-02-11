import importlib

from nicegui.testing import Screen

from .. import main


def test_markdown_message(screen: Screen) -> None:
    importlib.reload(main)

    screen.open('/')
    screen.wait(1)
    screen.should_contain('Try running')


def test_button_click(screen: Screen) -> None:
    importlib.reload(main)

    screen.open('/')
    screen.wait(1)
    screen.click('Click me')
    screen.should_contain('Button clicked!')


def test_sub_page(screen: Screen) -> None:
    importlib.reload(main)

    screen.open('/subpage')
    screen.wait(1)
    screen.should_contain('This is a subpage')
