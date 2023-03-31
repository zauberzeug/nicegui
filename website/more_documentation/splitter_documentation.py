from nicegui import ui


def main_demo() -> None:
    with ui.splitter() as splitter:
        with splitter.add_slot('before'):
            ui.label('This is some content on the left hand side.')
        with splitter.add_slot('after'):
            ui.label('This is some content on the right hand side.')
