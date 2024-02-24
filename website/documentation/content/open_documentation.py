from nicegui import ui

from . import doc


@doc.demo(ui.navigate.to)
def main_demo() -> None:
    url = 'https://github.com/zauberzeug/nicegui/'
    ui.button('Open GitHub', on_click=lambda: ui.navigate.to(url, new_tab=True))
