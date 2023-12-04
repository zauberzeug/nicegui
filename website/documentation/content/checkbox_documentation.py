from nicegui import ui

from . import doc


@doc.demo(ui.checkbox)
def main_demo() -> None:
    checkbox = ui.checkbox('check me')
    ui.label('Check!').bind_visibility_from(checkbox, 'value')


doc.reference(ui.checkbox)
