from nicegui import ui

from . import doc


@doc.demo(ui.toggle)
def main_demo() -> None:
    toggle1 = ui.toggle([1, 2, 3], value=1)
    toggle2 = ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(toggle1, 'value')


doc.reference(ui.toggle)
