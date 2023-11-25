from nicegui import ui

from ...model import UiElementDocumentation


class CheckboxDocumentation(UiElementDocumentation, element=ui.checkbox):

    def main_demo(self) -> None:
        checkbox = ui.checkbox('check me')
        ui.label('Check!').bind_visibility_from(checkbox, 'value')
