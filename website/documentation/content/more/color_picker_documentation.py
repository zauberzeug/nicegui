from nicegui import ui

from ...model import UiElementDocumentation


class ColorPickerDocumentation(UiElementDocumentation, element=ui.color_picker):

    def main_demo(self) -> None:
        with ui.button(icon='colorize') as button:
            ui.color_picker(on_pick=lambda e: button.style(f'background-color:{e.color}!important'))
