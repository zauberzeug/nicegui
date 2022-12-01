from menu import menu

from nicegui import ui


class page(ui.page):

    def __init__(self, route: str, navtitle: str) -> None:
        '''Custom page decorator to share the same styling and behavior across all pages'''
        super().__init__(route, title='Modularization Demo')
        self.navtitle = navtitle

    def create_content(self, *args, **kwargs) -> None:
        ui.colors(primary='#6E93D6', secondary='#53B689', accent='#111B1E', positive='#53B689')
        with ui.header().classes('justify-between text-white'):
            ui.label('Modularization Demo').classes('text-bold')
            ui.label(self.navtitle)
            with ui.row():
                menu()
        with ui.row().classes('absolute-center'):
            super().create_content(*args, **kwargs)
