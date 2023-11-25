from nicegui import ui

from ...model import UiElementDocumentation


class BadgeDocumentation(UiElementDocumentation, element=ui.badge):

    def main_demo(self) -> None:
        with ui.button('Click me!', on_click=lambda: badge.set_text(int(badge.text) + 1)):
            badge = ui.badge('0', color='red').props('floating')
