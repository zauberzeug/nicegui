from contextlib import contextmanager

from menu import menu

from nicegui import ui


@contextmanager
def frame(navtitle: str):
    """
    Custom page frame to share the same styling and behavior across all pages.

    Args:
        navtitle (str): The title to be displayed in the navigation bar.

    Usage:
        1. Call the `frame` function passing the `navtitle` as an argument.
        2. Customize the colors using the `ui.colors` function.
        3. Use the `ui.header` function to create a header section.
        4. Use the `ui.label` function to display the page title and `navtitle`.
        5. Use the `ui.row` function to create a row section.
        6. Call the `menu` function to add a menu section.
        7. Use the `ui.column` function to create a column section.
        8. Write the content of the page within the `yield` statement.

    Example:
        def my_page():
            with frame('My Page'):
                # Customize colors
                ui.colors(primary='#FF0000', secondary='#00FF00', accent='#0000FF', positive='#FFFF00')

                # Create header
                with ui.header().classes('justify-between text-white'):
                    ui.label('Modularization Example').classes('font-bold')
                    ui.label('My Page')

                # Create row
                with ui.row():
                    menu()

                # Create column
                with ui.column().classes('absolute-center items-center'):
                    # Page content goes here
                    ui.label('Welcome to My Page!')

        my_page()
    """
    ui.colors(primary='#6E93D6', secondary='#53B689', accent='#111B1E', positive='#53B689')
    with ui.header().classes('justify-between text-white'):
        ui.label('Modularization Example').classes('font-bold')
        ui.label(navtitle)
        with ui.row():
            menu()
    with ui.column().classes('absolute-center items-center'):
        yield
