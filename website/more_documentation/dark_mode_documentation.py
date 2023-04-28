from nicegui import ui


def main_demo() -> None:
    dark = ui.dark_mode()
    # ui.label('Switch mode:')
    # ui.button('Dark', on_click=dark.enable)
    # ui.button('Light', on_click=dark.disable)
    # END OF DEMO
    l = ui.label('Switch mode:')
    c = l.parent_slot.parent
    ui.button('Dark', on_click=lambda: (l.style('color: white'), c.style('background-color: var(--q-dark-page)')))
    ui.button('Light', on_click=lambda: (l.style('color: default'), c.style('background-color: default')))
