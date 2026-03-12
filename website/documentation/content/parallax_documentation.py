from nicegui import ui

from . import doc


@doc.demo(ui.parallax)
def main_demo() -> None:
    with ui.scroll_area():
        ui.label('Some text above...').classes('border h-32 w-full')
        with ui.parallax('https://cdn.quasar.dev/img/parallax2.jpg', height=200):
            ui.label('Text').classes('text-white')
        ui.label('Some text below...').classes('border h-32 w-full')


doc.reference(ui.parallax)
