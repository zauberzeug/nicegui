import theme
from message import message

from nicegui import ui


def create() -> None:
    """
    Creates example pages using the NiceGUI library.

    This function defines two example pages, '/a' and '/b', using the NiceGUI library. Each page is enclosed within a themed frame and displays a message.

    Example usage:
    ```
    create()
    ```

    Returns:
    None
    """
    @ui.page('/a')
    def example_page_a():
        with theme.frame('- Example A -'):
            message('Example A')

    @ui.page('/b')
    def example_page_b():
        with theme.frame('- Example B -'):
            message('Example B')
