from nicegui import ui

from ..model import UiElementDocumentation


class ContextMenuDocumentation(UiElementDocumentation, element=ui.context_menu):

    def main_demo(self) -> None:
        with ui.image('https://picsum.photos/id/377/640/360'):
            with ui.context_menu():
                ui.menu_item('Flip horizontally')
                ui.menu_item('Flip vertically')
                ui.separator()
                ui.menu_item('Reset')
