from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    ui.avatar('favorite_border', text_color='grey-11', square=True)
    ui.avatar('img:https://nicegui.io/logo_square.png', color='blue-2')


def more() -> None:
    @text_demo('Photos', '''
        To use a photo as an avatar, you can use `ui.image` within `ui.avatar`.
    ''')
    def photos() -> None:
        with ui.avatar():
            ui.image('https://robohash.org/robot?bgset=bg2')
