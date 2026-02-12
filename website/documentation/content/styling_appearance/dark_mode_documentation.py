from nicegui import ui

from ...windows import WINDOW_BG_COLORS
from .. import doc


@doc.demo(ui.dark_mode)
def main_demo() -> None:
    # dark = ui.dark_mode()
    # ui.label('Switch mode:')
    # ui.button('Dark', on_click=dark.enable)
    # ui.button('Light', on_click=dark.disable)
    # END OF DEMO
    label = ui.label('Switch mode:')
    container = label.parent_slot.parent
    ui.button('Dark', on_click=lambda: (
        label.style('color: white'),
        container.style(f'background-color: {WINDOW_BG_COLORS["browser"][1]}'),
    ))
    ui.button('Light', on_click=lambda: (
        label.style('color: black'),
        container.style(f'background-color: {WINDOW_BG_COLORS["browser"][0]}'),
    ))


@doc.demo('Binding to a switch', '''
    The value of the `ui.dark_mode` element can be bound to other elements like a `ui.switch`.
''')
def bind_to_switch() -> None:
    # dark = ui.dark_mode()
    # ui.switch('Dark mode').bind_value(dark)
    # END OF DEMO
    ui.switch('Dark mode', on_change=lambda e: (
        e.sender.style('color: white' if e.value else 'color: black'),
        e.sender.parent_slot.parent.style(f'background-color: {WINDOW_BG_COLORS["browser"][1 if e.value else 0]}'),
    ))


@doc.demo('Disable Dark Reader extension', '''
    NiceGUI sets a `<meta name="color-scheme">` tag to inform browsers and extensions about your app's color scheme.
    However, the [Dark Reader](https://darkreader.org/) browser extension may still transform your page.
    To prevent this, you can add a `<meta name="darkreader-lock">` tag using `ui.add_head_html`.
    Use `shared=True` to apply it to all pages, not just the current one.
    This is an [officially supported mechanism](https://github.com/darkreader/darkreader/blob/main/CONTRIBUTING.md#disabling-dark-reader-on-your-site).

    Note: Users can still enable Dark Reader manually in their extension settings if they prefer it over your dark theme.
''')
def darkreader_lock() -> None:
    # ui.add_head_html('<meta name="darkreader-lock">')

    ui.label('Dark Reader is disabled on this page.')


doc.reference(ui.dark_mode)
