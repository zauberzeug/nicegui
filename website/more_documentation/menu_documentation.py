from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    with ui.row().classes('w-full items-center'):
        result = ui.label().classes('mr-auto')
        with ui.button(on_click=lambda: menu.open()).props('icon=menu'):
            with ui.menu() as menu:
                ui.menu_item('Menu item 1', lambda: result.set_text('Selected item 1'))
                ui.menu_item('Menu item 2', lambda: result.set_text('Selected item 2'))
                ui.menu_item('Menu item 3 (keep open)',
                             lambda: result.set_text('Selected item 3'), auto_close=False)
                ui.separator()
                ui.menu_item('Close', on_click=menu.close)


def more() -> None:
    @text_demo('Custom Context Menu', '''
        Using Quasar's `context-menu` and `touch-position` props, you can create custom context menus.
    ''')
    def custom_context_menu() -> None:
        with ui.image('https://picsum.photos/id/377/640/360'):
            with ui.menu().props('context-menu touch-position'):
                ui.menu_item('Flip horizontally')
                ui.menu_item('Flip vertically')
                ui.separator()
                ui.menu_item('Reset')
