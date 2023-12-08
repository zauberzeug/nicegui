from nicegui import ui

from . import doc


@doc.demo(ui.color_picker)
def main_demo() -> None:
    with ui.button(icon='colorize') as button:
        ui.color_picker(on_pick=lambda e: button.style(f'background-color:{e.color}!important'))


doc.reference(ui.color_picker)
