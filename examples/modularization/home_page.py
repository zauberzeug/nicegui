from message import message

from nicegui import ui


def content() -> None:
    message('This is the home page.').classes('font-bold')
