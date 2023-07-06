from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    with ui.row():
        with ui.card().classes('w-48 h-32'):
            with ui.scroll_area().classes('w-full'):
                ui.label('I will scroll... ' * 10)

        with ui.card().classes('w-48 h-32'):
            ui.label('I will not scroll... ' * 10)


def more() -> None:

    @text_demo('Handling Scroll Events', '''
        You can use the `on_scroll` argument in `ui.scroll_area` to handle scroll events.
        The callback receives a `ScrollEventArguments` object with the following attributes:

        - `sender`: the scroll_area object that generated the event
        - `client`: the matching client
        - `info`: the scroll area information as described in Quasar documentation ScrollArea API   
          
        The scroll info is represented as a `ScrollInfo` dataclass
    ''')
    def scroll_events():
        number = ui.number(label='scroll position: ')
        with ui.card().classes('w-48 h-32'):
            with ui.scroll_area(on_scroll=lambda x: number.set_value(x.info.verticalPercentage)).classes('w-full'):
                ui.label('I will scroll... ' * 10)

    @text_demo('Setting the scroll position', '''
        You can use the `set_scroll_position` method of `ui.scroll_area` to programmatically set the scroll position.
        This can be useful for navigation or synchronization of multiple scroll_area elements
    ''')
    def scroll_events():
        with ui.row():
            with ui.column().classes('w-32'):
                number = ui.number(label='scroll position', value=0, min=0, max=1,
                                   on_change=lambda x: sa1.set_scroll_position(x.value)).classes('w-full')
                ui.button(icon='add', on_click=lambda: number.set_value(number.value + 0.1))
                ui.button(icon='remove', on_click=lambda: number.set_value(number.value - 0.1))

            with ui.card().classes('w-48 h-48'):
                with ui.scroll_area(
                        on_scroll=lambda x: sa2.set_scroll_position(x.info.verticalPercentage)
                ).classes('w-full') as sa1:
                    ui.label('I will scroll... ' * 100)

            with ui.card().classes('w-48 h-48'):
                with ui.scroll_area().classes('w-full') as sa2:
                    ui.label('I will scroll... ' * 100)


