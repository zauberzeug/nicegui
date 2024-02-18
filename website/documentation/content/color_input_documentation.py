from nicegui import ui

from . import doc


@doc.demo(ui.color_input)
def main_demo() -> None:
    label = ui.label('Change my color!')
    ui.color_input(label='Color', value='#000000',
                   on_change=lambda e: label.style(f'color:{e.value}'))


doc.reference(ui.color_input)
