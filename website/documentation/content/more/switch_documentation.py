from nicegui import ui

from ...model import UiElementDocumentation


class SwitchDocumentation(UiElementDocumentation, element=ui.switch):

    def main_demo(self) -> None:
        switch = ui.switch('switch me')
        ui.label('Switch!').bind_visibility_from(switch, 'value')
