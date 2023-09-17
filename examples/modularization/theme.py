from contextlib import contextmanager

from menu import menu

from nicegui import ui


@contextmanager
def frame(navtitle: str):
    '''Custom page frame to share the same styling and behavior across all pages'''
    ui.colors(primary='#6E93D6', secondary='#53B689', accent='#111B1E', positive='#53B689')
    with ui.header().classes('justify-between text-white'):
        with ui.row():
            menu()
        ui.label(navtitle)
        ui.label('Module Example').classes('font-bold')
        
    with ui.column().classes('absolute-center items-center'):
        yield
