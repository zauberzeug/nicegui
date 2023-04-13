from nicegui import ui


def main_demo() -> None:
    ui.button('Default', on_click=lambda: ui.colors())
    ui.button('Gray', on_click=lambda: ui.colors(primary='#555'))
