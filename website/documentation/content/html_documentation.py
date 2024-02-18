from nicegui import ui

from . import doc


@doc.demo(ui.html)
def main_demo() -> None:
    ui.html('This is <strong>HTML</strong>.')


doc.reference(ui.html)
