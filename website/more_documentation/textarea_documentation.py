from nicegui import ui


def main_demo() -> None:
    ui.textarea(label='Text', placeholder='start typing',
                on_change=lambda e: result.set_text('you typed: ' + e.value))
    result = ui.label()
