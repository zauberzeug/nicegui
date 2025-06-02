from drop_zone import DropZone as drop_zone

from nicegui import ui
from nicegui.events import DropZoneEventArguments


def say_hi(e: DropZoneEventArguments):
    print(e)
    if e.modifiers.shift:
        ui.notify('Shift key hold')
    else:
        ui.notify('Shift key not hold')
    ui.notify(e.path)


def say_hi_again(e: DropZoneEventArguments):
    print(e)
    ui.notify(f'again! {e.path}')


with ui.row().classes('flex-nowrap w-full flex-1 bg-blue-400'):
    with ui.column().classes('w-full h-screen'):
        with drop_zone(say_hi) as drop_zone1:
            ui.label("Drop it like it's hot (and try hold down Shift when dropping)")
        ui.label('Some text in between')
        with drop_zone(say_hi_again) as drop_zone2:
            ui.label("Drop it like it's hot again!")

drop_zone1.classes(add='relative whitespace-nowrap h-full w-full content-center text-center bg-cyan-400')
drop_zone1.hover_classes('bg-red-400')
drop_zone1.hover_overlay_classes('absolute inset-0 m-1 border-2 border-dashed border-neutral-700')

drop_zone2.classes(add='relative whitespace-nowrap h-full w-full content-center text-center bg-cyan-400')
drop_zone2.hover_overlay_classes('absolute inset-0 bg-gray-900 bg-opacity-75')

ui.add_css('''
    :root {
        --nicegui-default-padding: 0rem;
        --nicegui-default-gap: 0rem;
    }
''')

ui.run(
    native=True,
    reload=False,
    dark=True,
)
