#!/usr/bin/env python3
from router import Router

from nicegui import ui


@ui.page('/')  # normal index page (e.g. the entry point of the app)
@ui.page('/{_:path}')  # all other pages will be handled by the router but must be registered to also show the SPA index page
def main():
    """
    This function initializes a single-page application using the NiceGUI library.

    The function creates a router object and defines three routes using the `@router.add()` decorator.
    Each route corresponds to a different page in the application.
    The `show_one()`, `show_two()`, and `show_three()` functions are associated with their respective routes.
    These functions define the content to be displayed on each page using the `ui.label()` function.

    The function also adds navigation buttons to switch between the different pages.
    Clicking on a button triggers the corresponding route using the `router.open()` method.

    Finally, the function places the content to be displayed in a frame using the `router.frame()` method.

    Usage:
    1. Import the necessary modules and libraries.
    2. Call the `main()` function to start the application.

    Example:
    ```
    import nicegui as ui
    from nicegui.router import Router

    # Define the show_one(), show_two(), and show_three() functions

    if __name__ == '__main__':
        main()
    ```
    """
    router = Router()

    @router.add('/')
    def show_one():
        ui.label('Content One').classes('text-2xl')

    @router.add('/two')
    def show_two():
        ui.label('Content Two').classes('text-2xl')

    @router.add('/three')
    def show_three():
        ui.label('Content Three').classes('text-2xl')

    # adding some navigation buttons to switch between the different pages
    with ui.row():
        ui.button('One', on_click=lambda: router.open(show_one)).classes('w-32')
        ui.button('Two', on_click=lambda: router.open(show_two)).classes('w-32')
        ui.button('Three', on_click=lambda: router.open(show_three)).classes('w-32')

    # this places the content which should be displayed
    router.frame().classes('w-full p-4 bg-gray-100')


ui.run()
