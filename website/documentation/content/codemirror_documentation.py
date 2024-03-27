

from nicegui import ui

from . import doc


@doc.demo(ui.code_mirror)
def main_demo() -> None:
    ui.code_mirror()    


doc.reference(ui.code_mirror)