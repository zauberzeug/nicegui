from message import message

from nicegui import ui


def content() -> None:
    message('This is the home page.').classes('font-bold')
    ui.label('Use the menu on the top right to navigate.')
