from nicegui import ui
from nicegui.events import GenericEventArguments


def say_hi(e: GenericEventArguments):
    print('say_hi')
    ui.notify(e.args)


def say_hi_again(e: GenericEventArguments):
    print('say_hi_again')
    ui.notify(f'again! {e.args}')


with ui.row().classes('flex-nowrap w-full flex-1 bg-blue-400'):
    with ui.column().classes('w-full h-screen'):
        with ui.drop_zone() as drop_zone1:
            ui.label("Drop it like it's hot")
        ui.label('Some text in between')
        with ui.drop_zone() as drop_zone2:
            ui.label("Drop it like it's hot again!")

drop_zone1.classes(add='whitespace-nowrap h-full w-full content-center text-center bg-cyan-400')
drop_zone1.on('drop_zone', say_hi)
drop_zone2.classes(add='whitespace-nowrap h-full w-full content-center text-center bg-cyan-400')
drop_zone2.on('drop_zone', say_hi_again)

ui.add_css("""
    :root {
        --nicegui-default-padding: 0rem;
        --nicegui-default-gap: 0rem;
    }

    .dragover {
        border: 2px dashed #ccc;
        border-radius: 10px;
        border-color: #333;
        color: #333;
    }
""")

ui.run(
    native=True,
    reload=False,
    dark=True,
)
