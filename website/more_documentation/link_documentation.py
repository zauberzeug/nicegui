from nicegui import ui

from ..documentation_tools import text_demo
from ..style import link_target


def main_demo() -> None:
    ui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui')


def more() -> None:
    @text_demo('Navigate on large pages', '''
        To jump to a specific location within a page you can place linkable anchors with `ui.link_target('target_name')`
        or simply pass a NiceGUI element as link target.
    ''')
    def same_page_links():
        navigation = ui.row()
        # ui.link_target('target_A')
        link_target('target_A', '-10px')  # HIDE
        ui.label(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, '
            'sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
        )
        link_target('target_B', '70px')  # HIDE
        label_B = ui.label(
            'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
            'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
            'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
        )
        with navigation:
            ui.link('Goto A', '#target_A')
            # ui.link('Goto B', label_B)
            ui.link('Goto B', '#target_B')  # HIDE
