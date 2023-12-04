from nicegui import ui

from . import doc


@doc.demo(ui.mermaid)
def main_demo() -> None:
    ui.mermaid('''
    graph LR;
        A --> B;
        A --> C;
    ''')


doc.reference(ui.mermaid)
