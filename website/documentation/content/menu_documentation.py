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


@doc.demo('Menu with sub-menus', '''
    You can use a `ui.menu` nested inside a `ui.menu_item` to created nested sub-menus.
    The "anchor" and "self" props can be used to position the sub-menu.
    Make sure to disable `auto-close` on the corresponding menu item to keep the menu open while navigating the sub-menu.
''')
def submenus():
    with ui.button(icon='menu'):
        with ui.menu():
            ui.menu_item('Option 1')
            ui.menu_item('Option 2')
            with ui.menu_item('Option 3', auto_close=False):
                with ui.item_section().props('side'):
                    ui.icon('keyboard_arrow_right')
                with ui.menu().props('anchor="top end" self="top start" auto-close'):
                    ui.menu_item('Sub-option 1')
                    ui.menu_item('Sub-option 2')
                    ui.menu_item('Sub-option 3')


doc.reference(ui.menu, title='Reference for ui.menu')
doc.reference(ui.menu_item, title='Reference for ui.menu_item')
