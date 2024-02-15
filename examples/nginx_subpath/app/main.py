from nicegui import ui


@ui.page('/subpage')
def subpage():
    """
    Renders a subpage with a label, a link, and a button.

    This function is responsible for rendering a subpage in the NiceGUI application.
    It displays a label indicating that it is a subpage, a link to navigate back to the index page,
    and a button to go back to the previous page.

    Usage:
        - Call this function to render the subpage in the NiceGUI application.

    Example:
        subpage()
    """
    ui.label('This is a subpage').classes('text-h5 mx-auto mt-24')
    ui.link('Navigate to the index page.', '/').classes('text-lg mx-auto')
    ui.button('back', on_click=lambda: ui.open('/')).classes('mx-auto')


@ui.page('/')
def index():
    """
    Renders the main page of the NiceGUI app hosted on a subpath.

    This function creates a card element with centered text labels to demonstrate
    hosting a NiceGUI app on a subpath. The labels provide information about the app
    being available below "/nicegui" without the need for the code to know the subpath.

    Usage:
        - Call this function to render the main page of the app.

    Example:
        index()

    """
    with ui.card().classes('mx-auto p-24 items-center text-center'):
        ui.label('This demonstrates hosting of a NiceGUI app on a subpath.').classes('text-h5')
        ui.label('As you can see the entire app is available below "/nicegui".').classes('text-lg')
        ui.label('But the code here does not need to know that.').classes('text-lg')
        ui.link('Navigate to a subpage.', 'subpage').classes('text-lg')


ui.run()
