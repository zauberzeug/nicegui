from nicegui import ui

from ...model import UiElementDocumentation


class ExpansionDocumentation(UiElementDocumentation, element=ui.expansion):

    def main_demo(self) -> None:
        with ui.expansion('Expand!', icon='work').classes('w-full'):
            ui.label('inside the expansion')

    def more(self) -> None:
        @self.demo('Expansion with Custom Header', '''
            Instead of setting a plain-text title, you can fill the expansion header with UI elements by adding them to the "header" slot.
        ''')
        def expansion_with_custom_header():
            with ui.expansion() as expansion:
                with expansion.add_slot('header'):
                    ui.image('https://nicegui.io/logo.png').classes('w-16')
                ui.label('What a nice GUI!')
