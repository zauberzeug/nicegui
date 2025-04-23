from nicegui import ui

from . import doc


@doc.demo(ui.drop_zone)
def main_demo() -> None:
    with ui.drop_zone(on_drop=lambda e: ui.notify(e.path)).classes('whitespace-nowrap h-full w-full content-center text-center bg-blue-400'):
        ui.label('Drop a file or folder here')


@doc.demo('Modifier keys', '''
    You can also use modifier keys (shift, alt, ctrl, meta) to change what the trigger does.
''')
def modifier_keys() -> None:
    from nicegui import events

    def file_dropped(e: events.DropZoneEventArguments):
        if e.modifiers.shift:
            ui.notify(f'Shift is down: {e.path}')
        else:
            ui.notify(f'Shift is not down: {e.path}')

    with ui.drop_zone(on_drop=file_dropped).classes('h-full w-full content-center text-center bg-blue-400'):
        ui.label('Drop a file or folder here while holding down shift')


doc.reference(ui.drop_zone)
