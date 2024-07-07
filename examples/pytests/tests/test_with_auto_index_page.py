from nicegui.testing import Screen

from ..main import main_page, sub_page

# pylint: disable=missing-function-docstring


def test_markdown_message(screen: Screen) -> None:
    main_page()

    screen.open('/')
    screen.should_contain('Try running')


def test_button_click(screen: Screen) -> None:
    main_page()

    screen.open('/')
    screen.click('Click me')
    screen.should_contain('Button clicked!')


def test_sub_page(screen: Screen) -> None:
    sub_page()

    screen.open('/')
    screen.should_contain('This is a subpage')
