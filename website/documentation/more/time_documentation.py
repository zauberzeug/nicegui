from nicegui import ui

from ..model import UiElementDocumentation


class TimeDocumentation(UiElementDocumentation, element=ui.time):

    def main_demo(self) -> None:
        ui.time(value='12:00', on_change=lambda e: result.set_text(e.value))
        result = ui.label()
