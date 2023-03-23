from nicegui import ui


def main_demo() -> None:
    ui.date(value='2023-01-01', on_change=lambda e: result.set_text(e.value))
    result = ui.label()
