from nicegui import app, ui
from nicegui.events import GenericEventArguments


def say_hi(e: GenericEventArguments):
    print('say hi')
    print(e)
    ui.notify(e.args)


with ui.row().classes('flex-nowrap w-full flex-1 bg-blue-400'):
    with ui.column().classes('w-full h-screen'):
        with ui.drop_zone() as drop_zone:
            ui.label("Drop it like it's hot")

drop_zone.classes(replace='whitespace-nowrap h-full w-full content-center text-center bg-cyan-400')
drop_zone.on('drop_zone', say_hi)

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
