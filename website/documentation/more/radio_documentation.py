from nicegui import ui


def main_demo() -> None:
    radio1 = ui.radio([1, 2, 3], value=1).props('inline')
    radio2 = ui.radio({1: 'A', 2: 'B', 3: 'C'}).props('inline').bind_value(radio1, 'value')
