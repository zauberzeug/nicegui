from main import main_page
from nicegui.testing import Screen


def test_markdown_message(screen: Screen) -> None:
    """
    Test the markdown message on the main page.

    This function tests the behavior of the main_page() function by opening the main page
    and checking if it contains the expected markdown message.

    Args:
        screen (Screen): The screen object used for testing.

    Returns:
        None: This function does not return anything.

    Raises:
        AssertionError: If the expected markdown message is not found on the main page.
    """
    main_page()

    screen.open('/')
    screen.should_contain('Try running')


def test_button_click(screen: Screen) -> None:
    """
    Test the functionality of button click on the main page.

    This function tests the behavior of the button click on the main page of the application.
    It performs the following steps:
    1. Calls the main_page() function to set up the main page.
    2. Opens the main page by navigating to the root URL ('/').
    3. Clicks on the 'Click me' button.
    4. Verifies that the text 'Button clicked!' is present on the screen.

    Parameters:
    - screen (Screen): The screen object representing the application's UI.

    Returns:
    None
    """
    main_page()

    screen.open('/')
    screen.click('Click me')
    screen.should_contain('Button clicked!')
