#!/usr/bin/env python3
from nicegui import ui


@ui.page('/')
def main_page() -> None:
    """
    This function displays a main page with a markdown message and a button.

    The markdown message instructs the user to run `pytest` on the project.
    The button, when clicked, triggers a notification.

    Usage:
    - Call this function to display the main page.

    Example:
    >>> main_page()
    """

    ui.markdown('Try running `pytest` on this project!')
    ui.button('Click me', on_click=lambda: ui.notify('Button clicked!'))


if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
