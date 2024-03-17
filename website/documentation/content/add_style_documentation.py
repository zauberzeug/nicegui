from nicegui import ui

from . import doc


@doc.demo(ui.add_style)
def main_demo() -> None:
    ui.add_style('''
        .red {
            color: red;
        }
    ''')
    ui.label('This is red with CSS.').classes('red')


@doc.demo('Add SCSS', '''
    You can also use SCSS to define styles.
''')
def scss_demo() -> None:
    ui.add_style('''
        .green {
            background-color: lightgreen;
            .blue {
                color: blue;
            }
        }
    ''')
    with ui.element().classes('green'):
        ui.label('This is blue on green with SCSS.').classes('blue')


@doc.demo('Add SASS', '''
    You can also use the indented SASS syntax by setting the `indented` parameter to `True`.
''')
def sass_demo() -> None:
    ui.add_style('''
        .yellow
            background-color: yellow
            .purple
                color: purple
    ''', indented=True)
    with ui.element().classes('yellow'):
        ui.label('This is purple on yellow with SASS.').classes('purple')
