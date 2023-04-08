from nicegui import ui


def main_demo() -> None:
    ui.button('Click me!', on_click=lambda: ui.notify(f'You clicked me!'))
