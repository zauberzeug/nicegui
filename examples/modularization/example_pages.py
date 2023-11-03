import theme
from message import message

from nicegui import ui


def create() -> None:

    @ui.page('/a')
    def example_page_a():
        with theme.frame('- Example A -'):
            message('Example A')

    @ui.page('/b')
    def example_page_b():
        with theme.frame('- Example B -'):
            message('Example B')
