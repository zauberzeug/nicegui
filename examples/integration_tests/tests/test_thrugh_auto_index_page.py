from nicegui import Client
from nicegui.testing import SeleniumScreen

from ..main import main_page, sub_page


def test_markdown_message(screen: SeleniumScreen) -> None:
    main_page()

    screen.open('/')
    screen.should_contain('Try running')


def test_button_click(screen: SeleniumScreen) -> None:
    main_page()

    screen.open('/')
    screen.click('Click me')
    screen.should_contain('Button clicked!')


def test_sub_page(screen: SeleniumScreen) -> None:
    sub_page()

    screen.open('/')
    screen.should_contain('This is a subpage')
