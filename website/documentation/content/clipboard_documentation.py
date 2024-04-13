from nicegui import ui

from . import doc


@doc.demo('Read and write to the clipboard', '''
    The following demo shows how to use `ui.clipboard.read()` and `ui.clipboard.write()` to interact with the clipboard.
    Note that your browser may ask for permission to access the clipboard or may not support this feature at all.
''')
def main_demo() -> None:
    ui.button('Write', on_click=lambda: ui.clipboard.write('Hi!'))

    async def read() -> None:
        ui.notify(await ui.clipboard.read())
    ui.button('Read', on_click=read)


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
