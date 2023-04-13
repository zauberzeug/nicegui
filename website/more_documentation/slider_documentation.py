from nicegui import ui


def main_demo() -> None:
    slider = ui.slider(min=0, max=100, value=50)
    ui.label().bind_text_from(slider, 'value')
