from nicegui import ui

from . import doc


@doc.demo(ui.separator)
def main_demo() -> None:
    ui.label('text above')
    ui.separator()
    ui.label('text below')


doc.reference(ui.separator)
