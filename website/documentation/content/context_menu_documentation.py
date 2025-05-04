from nicegui import ui

from . import doc


@doc.demo(ui.context_menu)
def main_demo() -> None:
    with ui.image('https://picsum.photos/id/377/640/360'):
        with ui.context_menu():
            ui.menu_item('Flip horizontally')
            ui.menu_item('Flip vertically')
            ui.separator()
            ui.menu_item('Reset', auto_close=False)


@doc.demo('Context menus with dynamic content', '''
    To show a context menu with content that changes dynamically, e.g. based on the position of the mouse,
    it is recommended to re-use the same context menu instance.
    This demo shows how to clear the context menu and add new items to it.
''')
def update_context_menu() -> None:
    from nicegui import events

    def update_menu(e: events.MouseEventArguments) -> None:
        context_menu.clear()
        with context_menu:
            ui.menu_item(f'Add circle at ({e.image_x:.0f}, {e.image_y:.0f})')

    source = 'https://picsum.photos/id/377/640/360'
    with ui.interactive_image(source, on_mouse=update_menu, events=['contextmenu']):
        context_menu = ui.context_menu()


doc.reference(ui.context_menu)
