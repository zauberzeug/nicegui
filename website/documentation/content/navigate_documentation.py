from nicegui import ui

from . import doc


@doc.demo(ui.navigate)
def main_demo() -> None:
    with ui.row():
        ui.button('Back', on_click=ui.navigate.back)
        ui.button('Forward', on_click=ui.navigate.forward)
        ui.button('Reload', on_click=ui.navigate.reload)
        ui.button(icon='savings',
                  on_click=lambda: ui.navigate.to('https://github.com/sponsors/zauberzeug'))


@doc.demo(ui.navigate.to)
def open_github() -> None:
    url = 'https://github.com/zauberzeug/nicegui/'
    ui.button('Open GitHub', on_click=lambda: ui.navigate.to(url, new_tab=True))


@doc.demo('Push and replace URLs', '''
    The `history` API allows you to push and replace URLs to the browser history.

    While the `history.push` method pushes a new URL to the history,
    the `history.replace` method replaces the current URL.

    See `JavaScript's History API <https://developer.mozilla.org/en-US/docs/Web/API/History>`_ for more information.

    *Added in version 2.13.0*
''')
def history_demo() -> None:
    ui.button('Push URL', on_click=lambda: ui.navigate.history.push('/a'))
    ui.button('Replace URL', on_click=lambda: ui.navigate.history.replace('/b'))
