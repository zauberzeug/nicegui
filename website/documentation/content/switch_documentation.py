from nicegui import ui

from . import doc


@doc.demo(ui.switch)
def main_demo() -> None:
    switch = ui.switch('switch me')
    ui.label('Switch!').bind_visibility_from(switch, 'value')


doc.reference(ui.switch)
