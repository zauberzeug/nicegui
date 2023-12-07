from nicegui import ui

from . import doc


@doc.demo(ui.knob)
def main_demo() -> None:
    knob = ui.knob(0.3, show_value=True)

    with ui.knob(color='orange', track_color='grey-2').bind_value(knob, 'value'):
        ui.icon('volume_up')


doc.reference(ui.knob)
