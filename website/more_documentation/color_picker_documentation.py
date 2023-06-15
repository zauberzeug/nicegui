from nicegui import ui


def main_demo() -> None:
    picker = ui.color_picker(on_pick=lambda e: button.style(f'background-color:{e.color}!important'))
    button = ui.button(on_click=picker.open, icon='colorize')
