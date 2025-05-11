from nicegui import ui

from . import doc


@doc.demo('Read and write to the clipboard', '''
    The following demo shows how to use `ui.clipboard.read()`, `ui.clipboard.write()` and `ui.clipboard.read_image()` to interact with the clipboard.

    Because auto-index page can be accessed by multiple browser tabs simultaneously, reading the clipboard is not supported on this page.
    This is only possible within page-builder functions decorated with `ui.page`, as shown in this demo.

    Note that your browser may ask for permission to access the clipboard or may not support this feature at all.
''')
def main_demo() -> None:
    # @ui.page('/')
    # async def index():
    with ui.column():  # HIDE
        ui.button('Write Text', on_click=lambda: ui.clipboard.write('Hi!'))

        async def read() -> None:
            ui.notify(await ui.clipboard.read())
        ui.button('Read Text', on_click=read)

        async def read_image() -> None:
            img = await ui.clipboard.read_image()
            if not img:
                ui.notify('You must copy an image to clipboard first.')
            else:
                image.set_source(img)
        ui.button('Read Image', on_click=read_image)
        image = ui.image().classes('w-72')


@doc.demo('Client-side clipboard', '''
    In order to avoid the round-trip to the server, you can also use the client-side clipboard API directly.
    This might be supported by more browsers because the clipboard access is directly triggered by a user action.
''')
def client_side_clipboard() -> None:
    ui.button('Write').on('click', js_handler='''
        () => navigator.clipboard.writeText("Ho!")
    ''')
    ui.button('Read').on('click', js_handler='''
        async () => emitEvent("clipboard", await navigator.clipboard.readText())
    ''')
    ui.on('clipboard', lambda e: ui.notify(e.args))
