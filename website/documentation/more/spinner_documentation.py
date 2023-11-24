from nicegui import ui

from ..model import UiElementDocumentation


class SpinnerDocumentation(UiElementDocumentation, element=ui.spinner):

    def main_demo(self) -> None:
        with ui.row():
            ui.spinner(size='lg')
            ui.spinner('audio', size='lg', color='green')
            ui.spinner('dots', size='lg', color='red')
