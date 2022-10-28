from nicegui import ui

from menu import menu


def navbar(navtitle: str = 'No Title') -> None:
    ui.colors(primary='#6E93D6', secondary='#53B689', accent='#111B1E', positive='#53B689')
    with ui.row().classes('fit bg-primary q-py-sm q-px-md q-ma-none no-wrap shadow-2', remove='q-gutter-sm').style('gap:0'):
        ui.label('Modularization Demo').classes('text-white text-weight-bold col-3')
        with ui.row().classes('col-6'):
            ui.label(navtitle).classes('text-white text-center fit')
        with ui.row().classes('col-3 justify-end'):
            menu()
