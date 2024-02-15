from message import message


def content() -> None:
    """
    This function displays the content of the home page.

    It shows a message with the text "This is the home page." in a bold font.

    Usage:
        content()
    """
    message('This is the home page.').classes('font-bold')
