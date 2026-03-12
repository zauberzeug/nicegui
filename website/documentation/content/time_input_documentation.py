from nicegui import ui

from . import doc


@doc.demo(ui.time_input)
def main_demo() -> None:
    time = ui.time_input('Time', value='12:30')
    ui.label().bind_text_from(time, 'value', lambda v: f'time: {v}')


doc.reference(ui.time_input)
