from nicegui import ui

from ...model import UiElementDocumentation


class LinearProgressDocumentation(UiElementDocumentation, element=ui.linear_progress):

    def main_demo(self) -> None:
        slider = ui.slider(min=0, max=1, step=0.01, value=0.5)
        ui.linear_progress().bind_value_from(slider, 'value')
