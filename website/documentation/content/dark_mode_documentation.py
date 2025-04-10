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
    label = ui.label('Switch mode:')
    container = label.parent_slot.parent
    ui.button('Dark', on_click=lambda: (
        label.style('color: white'),
        container.style(f'background-color: {WINDOW_BG_COLORS["browser"][1]}'),
    ))
    ui.button('Light', on_click=lambda: (
        label.style('color: black'),
        container.style(f'background-color: {WINDOW_BG_COLORS["browser"][0]}'),
    ))


@doc.demo('Binding to a switch', '''
    The value of the `ui.dark_mode` element can be bound to other elements like a `ui.switch`.
''')
def bind_to_switch() -> None:
    # dark = ui.dark_mode()
    # ui.switch('Dark mode').bind_value(dark)
    # END OF DEMO
    ui.switch('Dark mode', on_change=lambda e: (
        e.sender.style('color: white' if e.value else 'color: black'),
        e.sender.parent_slot.parent.style(f'background-color: {WINDOW_BG_COLORS["browser"][1 if e.value else 0]}'),
    ))


doc.reference(ui.dark_mode)
