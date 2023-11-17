from nicegui import ui


def main_demo() -> None:
    checkbox = ui.checkbox('check me')
    ui.label('Check!').bind_visibility_from(checkbox, 'value')
