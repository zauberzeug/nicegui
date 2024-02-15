from nicegui import ui


class message(ui.label):
    """
    A custom label widget for displaying messages.

    This class extends the `ui.label` class and provides additional functionality
    for displaying messages. It sets the text of the label and applies CSS classes
    to style the label.

    Parameters:
        text (str): The text to be displayed in the label.

    Example:
        # Create a message label with the text "Hello, World!"
        msg = message("Hello, World!")

    """

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.classes('text-h4 text-grey-8')
