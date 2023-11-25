from nicegui import ui

from ...model import UiElementDocumentation


class MermaidDocumentation(UiElementDocumentation, element=ui.mermaid):

    def main_demo(self) -> None:
        ui.mermaid('''
        graph LR;
            A --> B;
            A --> C;
        ''')
