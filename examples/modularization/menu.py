from nicegui import ui


def menu() -> None:
    """
    Renders a menu with links to different pages.

    This function is responsible for rendering a menu with links to different pages.
    It uses the `ui.link` function to create each link and applies a CSS class to
    style the links.

    Usage:
        Call this function to render the menu on a web page.

    Example:
        menu()

    """
    ui.link('Home', '/').classes(replace='text-white')
    ui.link('A', '/a').classes(replace='text-white')
    ui.link('B', '/b').classes(replace='text-white')
    ui.link('C', '/c').classes(replace='text-white')
