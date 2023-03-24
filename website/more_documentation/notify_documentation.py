from nicegui import ui


def main_demo() -> None:
    ui.button('Say hi!', on_click=lambda: ui.notify('Hi!', close_button='OK'))
