from nicegui import ui

from ..windows import WINDOW_BG_COLORS
from . import doc


@doc.demo(ui.dark_mode)
def main_demo() -> None:
    # dark = ui.dark_mode()
    # ui.label('Switch mode:')
    # ui.button('Dark', on_click=dark.enable)
    # ui.button('Light', on_click=dark.disable)
    # END OF DEMO
    l = ui.label('Switch mode:')
    c = l.parent_slot.parent
    ui.button('Dark', on_click=lambda: (
        l.style('color: white'),
        c.style(f'background-color: {WINDOW_BG_COLORS["browser"][1]}'),
    ))
    ui.button('Light', on_click=lambda: (
        l.style('color: black'),
        c.style(f'background-color: {WINDOW_BG_COLORS["browser"][0]}'),
    ))


doc.reference(ui.dark_mode)
