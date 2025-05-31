from nicegui import ui

from . import doc


@doc.demo(ui.time_input)
def main_demo() -> None:
    label = ui.label('time: 12:30')
    ui.time_input(label='Time', value='12:30',
                  on_change=lambda e: label.set_text(f'time: {e.value}'))


doc.reference(ui.time_input)
