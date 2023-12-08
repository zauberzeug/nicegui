from nicegui import ui

from . import doc


@doc.demo(ui.circular_progress)
def main_demo() -> None:
    slider = ui.slider(min=0, max=1, step=0.01, value=0.5)
    ui.circular_progress().bind_value_from(slider, 'value')


@doc.demo('Nested Elements', '''
    You can put any element like icon, button etc inside a circular progress using the `with` statement.
    Just make sure it fits the bounds and disable the default behavior of showing the value.
''')
def icon() -> None:
    with ui.row().classes('items-center m-auto'):
        with ui.circular_progress(value=0.1, show_value=False) as progress:
            ui.button(
                icon='star',
                on_click=lambda: progress.set_value(progress.value + 0.1)
            ).props('flat round')
        ui.label('click to increase progress')


doc.reference(ui.circular_progress)
