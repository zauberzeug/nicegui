from nicegui import ui

from ...model import UiElementDocumentation


class AvatarDocumentation(UiElementDocumentation, element=ui.avatar):

    def main_demo(self) -> None:
        ui.avatar('favorite_border', text_color='grey-11', square=True)
        ui.avatar('img:https://nicegui.io/logo_square.png', color='blue-2')

    def more(self) -> None:
        @self.demo('Photos', '''
            To use a photo as an avatar, you can use `ui.image` within `ui.avatar`.
        ''')
        def photos() -> None:
            with ui.avatar():
                ui.image('https://robohash.org/robot?bgset=bg2')
