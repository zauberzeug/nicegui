from nicegui import ui


def main_demo() -> None:
    ui.mermaid('''
    graph LR;
        A --> B;
        A --> C;
    ''')
