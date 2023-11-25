from nicegui import ui

from ...model import UiElementDocumentation


class OpenDocumentation(UiElementDocumentation, element=ui.open):

    def main_demo(self) -> None:
        @ui.page('/yet_another_page')
        def yet_another_page():
            ui.label('Welcome to yet another page')
            ui.button('RETURN', on_click=lambda: ui.open('documentation#open'))

        ui.button('REDIRECT', on_click=lambda: ui.open(yet_another_page))
