from nicegui import ui

from . import doc


@doc.demo(ui.scroll_area)
def main_demo() -> None:
    with ui.row():
        with ui.scroll_area().classes('w-32 h-32 border'):
            ui.label('I scroll. ' * 20)
        with ui.column().classes('p-4 w-32 h-32 border'):
            ui.label('I will not scroll. ' * 10)


@doc.demo('Handling Scroll Events', '''
    You can use the `on_scroll` argument in `ui.scroll_area` to handle scroll events.
    The callback receives a `ScrollEventArguments` object with the following attributes:

    - `sender`: the scroll area that generated the event
    - `client`: the matching client
    - additional arguments as described in [Quasar's documentation for the ScrollArea API](https://quasar.dev/vue-components/scroll-area/#qscrollarea-api)
''')
def scroll_events():
    position = ui.number('scroll position:').props('readonly')
    with ui.card().classes('w-32 h-32'):
        with ui.scroll_area(on_scroll=lambda e: position.set_value(e.vertical_percentage)):
            ui.label('I scroll. ' * 20)


@doc.demo('Setting the scroll position', '''
    You can use `scroll_to` to programmatically set the scroll position.
    This can be useful for navigation or synchronization of multiple scroll areas.
''')
def scroll_position():
    ui.number('position', value=0, min=0, max=1, step=0.1,
              on_change=lambda e: area1.scroll_to(percent=e.value)).classes('w-32')

    with ui.row():
        with ui.card().classes('w-32 h-48'):
            with ui.scroll_area(on_scroll=lambda e: area2.scroll_to(percent=e.vertical_percentage)) as area1:
                ui.label('I scroll. ' * 20)

        with ui.card().classes('w-32 h-48'):
            with ui.scroll_area() as area2:
                ui.label('I scroll. ' * 20)


doc.reference(ui.scroll_area)
