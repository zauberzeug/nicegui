from nicegui import ui


def main_demo() -> None:
    def set_background(color: str) -> None:
        ui.query('body').style(f'background-color: {color}')

    # ui.button('Blue', on_click=lambda: set_background('#ddeeff'))
    # ui.button('Orange', on_click=lambda: set_background('#ffeedd'))
    # END OF DEMO
    ui.button('Blue', on_click=lambda e: e.sender.parent_slot.parent.style('background-color: #ddeeff'))
    ui.button('Orange', on_click=lambda e: e.sender.parent_slot.parent.style('background-color: #ffeedd'))
