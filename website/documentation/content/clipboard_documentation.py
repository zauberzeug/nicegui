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
