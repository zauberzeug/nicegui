from nicegui import ui

from . import doc


@doc.demo(ui.context_menu)
def main_demo() -> None:
    with ui.image('https://picsum.photos/id/377/640/360'):
        with ui.context_menu():
            with ui.list():
                ui.menu_item('Flip horizontally').props('clickable')
                ui.menu_item('Flip vertically').props('clickable')
                ui.separator()
                ui.menu_item('Reset', auto_close=False).props('clickable')


doc.reference(ui.context_menu)
