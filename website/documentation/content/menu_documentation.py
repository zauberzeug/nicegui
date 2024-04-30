from nicegui import ui

from . import doc


@doc.demo(ui.menu)
def main_demo() -> None:
    with ui.row().classes('w-full items-center'):
        result = ui.label().classes('mr-auto')
        with ui.button(icon='menu'):
            with ui.menu() as menu:
                ui.menu_item('Menu item 1', lambda: result.set_text('Selected item 1'))
                ui.menu_item('Menu item 2', lambda: result.set_text('Selected item 2'))
                ui.menu_item('Menu item 3 (keep open)',
                             lambda: result.set_text('Selected item 3'), auto_close=False)
                ui.separator()
                ui.menu_item('Close', menu.close)


@doc.demo('Client-side auto-close', '''
    Use the `auto-close` prop to automatically close the menu on any click event directly without a server round-trip.
''')
def auto_close():
    with ui.button(icon='menu'):
        with ui.menu().props('auto-close'):
            toggle = ui.toggle(['fastfood', 'cake', 'icecream'], value='fastfood')
    ui.icon('', size='md').bind_name_from(toggle, 'value')


doc.reference(ui.menu)
