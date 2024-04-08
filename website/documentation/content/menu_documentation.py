from nicegui import ui

from . import doc


@doc.demo(ui.menu)
def main_demo() -> None:
    with ui.row().classes('w-full items-center'):
        result = ui.label().classes('mr-auto')
        with ui.button(icon='menu'):
            with ui.menu() as menu:
                ui.item('Menu item 1', on_click=lambda: result.set_text('Selected item 1'))
                ui.item('Menu item 2', on_click=lambda: result.set_text('Selected item 2'))
                ui.item('Menu item 3', on_click=lambda: result.set_text('Selected item 3'))
                ui.separator()
                ui.item('Close', on_click=menu.close)


doc.reference(ui.menu)
