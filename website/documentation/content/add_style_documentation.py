from nicegui import ui

from . import doc


@doc.demo(ui.add_css)
def main_demo() -> None:
    ui.add_css('''
        .red {
            color: red;
        }
    ''')
    ui.label('This is red with CSS.').classes('red')
