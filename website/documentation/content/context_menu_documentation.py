from nicegui import ui

from . import doc


@doc.demo(ui.context_menu)
def main_demo() -> None:
    with ui.image('https://picsum.photos/id/377/640/360'):
        with ui.context_menu(auto_close=True):
            ui.item('Flip horizontally').props('clickable')
            ui.item('Flip vertically').props('clickable')
            ui.separator()
            ui.item('Reset').props('clickable')


doc.reference(ui.context_menu)
