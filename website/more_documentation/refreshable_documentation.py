from nicegui import ui


def main_demo() -> None:
    import random

    numbers = []

    @ui.refreshable
    def number_ui() -> None:
        ui.label(', '.join(str(n) for n in sorted(numbers)))

    def add_number() -> None:
        numbers.append(random.randint(0, 100))
        number_ui.refresh()

    number_ui()
    ui.button('Add random number', on_click=add_number)
