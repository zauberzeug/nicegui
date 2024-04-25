import theme
from message import message

from nicegui import ui


def create() -> None:
    @ui.page('/a')
    def page_a():
        with theme.frame('- Page A -'):
            message('Page A')
            ui.label('This page is defined in a function.')
