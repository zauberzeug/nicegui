from nicegui import ui

from ..model import UiElementDocumentation


class CircularProgressDocumentation(UiElementDocumentation, element=ui.circular_progress):

    def main_demo(self) -> None:
        slider = ui.slider(min=0, max=1, step=0.01, value=0.5)
        ui.circular_progress().bind_value_from(slider, 'value')

    def more(self) -> None:
        @self.demo('Nested Elements', '''
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
