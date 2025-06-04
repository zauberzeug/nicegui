import time
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

    See [JavaScript's History API](https://developer.mozilla.org/en-US/docs/Web/API/History) for more information.

    *Added in version 2.13.0*
''')
def history_demo() -> None:
    ui.button('Push URL', on_click=lambda: ui.navigate.history.push('/a'))
    ui.button('Replace URL', on_click=lambda: ui.navigate.history.replace('/b'))


@doc.demo('Soft reload', '''
    The `soft_reload` parameter allows you to reload the current page without reloading the entire page as if pressing F5.
    When set to `True`, it uses NiceGUI's soft reload mechanism to pull in the new content, and the browser does not actually reload the entire page.

    Notice how in the below demo, when clicking the "Soft reload" button, the page only flash very briefly, but the last loaded time is updated.
    Compared to a normal reload, which is equivalent to clicking the reload button in the browser, which takes longer in comparison, especially on a slow network connection.

    *Added in version 2.20.0*
''')
def soft_reload_demo() -> None:
    ui.label(f'Page last loaded at: {time.strftime("%H:%M:%S")}')
    ui.button('Soft reload', on_click=lambda: ui.navigate.reload(soft_reload=True))
    ui.button('Normal (hard) reload', on_click=lambda: ui.navigate.reload())


@doc.demo('Soft reload to another page', '''
    The `soft_reload` parameter can also be used to navigate to another page without reloading the entire page.
''')
def soft_reload_to_page_demo() -> None:
    @ui.page('/soft_reload_demo')
    def soft_reload_demo_page() -> None:
        ui.label('This is the soft reload demo page.')
        ui.label(f'Page last loaded at: {time.strftime("%H:%M:%S")}')
        ui.button('Soft reload to original page', on_click=lambda: ui.navigate.to(
            '/documentation/navigate', soft_reload=True))
        ui.button('Normal (hard) reload to original page', on_click=lambda: ui.navigate.to('/documentation/navigate'))
    ui.label(f'Page last loaded at: {time.strftime("%H:%M:%S")}')
    ui.button('Soft reload to another page', on_click=lambda: ui.navigate.to('/soft_reload_demo', soft_reload=True))
    ui.button('Normal (hard) reload to another page', on_click=lambda: ui.navigate.to('/soft_reload_demo'))
