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


@doc.demo('Updating context menu items', '''
    Only the first `ui.context_menu` instance is respected by Quasar. 
          
    Therefore, the following paradigm is used to update the context menu items:
          
    - Create a new context menu while keeping a reference (`with ui.context_menu() as cmenu:`).
    - Clear any existing items in the context menu (`cmenu.clear()`).
    - Add new items to the existing context menu (`with cmenu: ...`).
''')
def update_context_menu() -> None:
    with ui.card().classes('w-full'):
        ui.label('Right-click to see the context menu.')
        with ui.context_menu() as cmenu:
            ui.menu_item('Original item')

    def update_items(new_item: str) -> None:
        cmenu.clear()
        with cmenu:
            ui.menu_item(new_item)

    with ui.row():
        ui.button('Set new menu items', on_click=lambda: update_items('New item'))
        ui.button('Reset', on_click=lambda: update_items('Original item'))


doc.reference(ui.context_menu)
