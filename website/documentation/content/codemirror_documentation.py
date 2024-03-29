from nicegui import ui

from . import doc


@doc.demo(ui.codemirror)
def main_demo() -> None:
    ui.codemirror()


doc.reference(ui.codemirror)
