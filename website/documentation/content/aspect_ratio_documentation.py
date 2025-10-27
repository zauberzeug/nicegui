from nicegui import ui

from . import doc


@doc.demo(ui.aspect_ratio)
def main_demo() -> None:
    with ui.aspect_ratio(ratio=16 / 9):
        with ui.card():
            ui.icon('live_tv')
            ui.label('16:9 content')


doc.reference(ui.aspect_ratio)
