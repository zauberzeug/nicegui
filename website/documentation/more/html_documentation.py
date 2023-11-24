from nicegui import ui

from ..model import UiElementDocumentation


class HtmlDocumentation(UiElementDocumentation, element=ui.html):

    def main_demo(self) -> None:
        ui.html('This is <strong>HTML</strong>.')
