import importlib

from nicegui.testing import SeleniumScreen

from .. import main


def test_markdown_message(screen: SeleniumScreen) -> None:
    importlib.reload(main)

    screen.open('/')
    screen.wait(1)
    screen.should_contain('Try running')


def test_button_click(screen: SeleniumScreen) -> None:
    importlib.reload(main)

    screen.open('/')
    screen.wait(1)
    screen.click('Click me')
    screen.should_contain('Button clicked!')


def test_sub_page(screen: SeleniumScreen) -> None:
    importlib.reload(main)

    screen.open('/subpage')
    screen.wait(1)
    screen.should_contain('This is a subpage')


def test_with_connected(screen: SeleniumScreen) -> None:
    importlib.reload(main)

    screen.open('/with_connected')
    screen.wait(1)
    screen.should_contain('This is an async connection demo')
    screen.wait(1)
    screen.should_contain('Connected!')
