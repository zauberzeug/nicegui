from main import main_page
from nicegui.testing import Screen


def test_markdown_message(screen: Screen) -> None:
    main_page()

    screen.open('/')
    screen.should_contain('Try running')


def test_button_click(screen: Screen) -> None:
    main_page()

    screen.open('/')
    screen.click('Click me')
    screen.should_contain('Button clicked!')
