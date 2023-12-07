from nicegui import ui

from . import doc


@doc.demo(ui.time)
def main_demo() -> None:
    ui.time(value='12:00', on_change=lambda e: result.set_text(e.value))
    result = ui.label()


doc.reference(ui.time)
