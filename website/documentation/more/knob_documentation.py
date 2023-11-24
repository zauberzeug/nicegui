from nicegui import ui

from ..model import UiElementDocumentation


class KnobDocumentation(UiElementDocumentation, element=ui.knob):

    def main_demo(self) -> None:
        knob = ui.knob(0.3, show_value=True)

        with ui.knob(color='orange', track_color='grey-2').bind_value(knob, 'value'):
            ui.icon('volume_up')
