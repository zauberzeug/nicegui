from nicegui import ui


def main_demo() -> None:
    switch = ui.switch('switch me')
    ui.label('Switch!').bind_visibility_from(switch, 'value')
