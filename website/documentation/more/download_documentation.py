from nicegui import ui

from ..model import UiElementDocumentation


class DownloadDocumentation(UiElementDocumentation, element=ui.download):

    def main_demo(self) -> None:
        ui.button('Logo', on_click=lambda: ui.download('https://nicegui.io/logo.png'))

    def more(self) -> None:
        @self.demo('Download raw bytes from memory', '''
            The `download` function can also be used to download raw bytes from memory.
        ''')
        def raw_bytes():
            ui.button('Download', on_click=lambda: ui.download(b'Hello World', 'hello.txt'))
