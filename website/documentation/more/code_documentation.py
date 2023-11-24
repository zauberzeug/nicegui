from nicegui import ui

from ..model import UiElementDocumentation


class CodeDocumentation(UiElementDocumentation, element=ui.code):

    def main_demo(self) -> None:
        ui.code('''
            from nicegui import ui
            
            ui.label('Code inception!')
                
            ui.run()
        ''').classes('w-full')
