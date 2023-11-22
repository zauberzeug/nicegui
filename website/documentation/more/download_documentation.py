from nicegui import ui


def main_demo() -> None:
    ui.button('NiceGUI Logo', on_click=lambda: ui.download('https://nicegui.io/logo.png'))
