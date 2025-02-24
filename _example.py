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
        with ui.drop_zone(say_hi) as drop_zone1:
            ui.label('Drop it like it\'s hot')
        ui.label('Some text in between')
        with ui.drop_zone() as drop_zone2:
            ui.label('Drop it like it\'s hot again!')

drop_zone1.classes(add='whitespace-nowrap h-full w-full content-center text-center bg-cyan-400')
drop_zone2.classes(add='whitespace-nowrap h-full w-full content-center text-center bg-cyan-400')

ui.add_css("""
    :root {
        --nicegui-default-padding: 0rem;
        --nicegui-default-gap: 0rem;
    }
""")

ui.run(
    native=True,
    reload=False,
    dark=True,
)
