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


@doc.demo(ui.add_scss)
def scss_demo() -> None:
    ui.add_scss('''
        .green {
            background-color: lightgreen;
            .blue {
                color: blue;
            }
        }
    ''')
    with ui.element().classes('green'):
        ui.label('This is blue on green with SCSS.').classes('blue')


@doc.demo(ui.add_sass)
def sass_demo() -> None:
    ui.add_sass('''
        .yellow
            background-color: yellow
            .purple
                color: purple
    ''')
    with ui.element().classes('yellow'):
        ui.label('This is purple on yellow with SASS.').classes('purple')
