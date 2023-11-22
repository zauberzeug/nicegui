from nicegui import ui


def main_demo() -> None:
    knob = ui.knob(0.3, show_value=True)

    with ui.knob(color='orange', track_color='grey-2').bind_value(knob, 'value'):
        ui.icon('volume_up')
