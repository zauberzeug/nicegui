from nicegui import ui

from ..model import UiElementDocumentation


class SeparatorDocumentation(UiElementDocumentation, element=ui.separator):

    def main_demo(self) -> None:
        ui.label('text above')
        ui.separator()
        ui.label('text below')
