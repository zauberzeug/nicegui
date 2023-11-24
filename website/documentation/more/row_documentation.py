from nicegui import ui

from ..model import UiElementDocumentation


class RowDocumentation(UiElementDocumentation, element=ui.row):

    def main_demo(self) -> None:
        with ui.row():
            ui.label('label 1')
            ui.label('label 2')
            ui.label('label 3')
