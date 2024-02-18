from nicegui import ui

from . import doc


@doc.demo(ui.open)
def main_demo() -> None:
    url = 'https://github.com/zauberzeug/nicegui/'
    ui.button('Open GitHub', on_click=lambda: ui.open(url, new_tab=True))
