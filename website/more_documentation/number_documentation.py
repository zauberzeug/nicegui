from nicegui import ui


def main_demo() -> None:
    ui.number(label='Number', value=3.1415927, format='%.2f',
              on_change=lambda e: result.set_text(f'you entered: {e.value}'))
    result = ui.label()
