from nicegui import ui


@ui.page('/subpage')
def subpage():
    ui.label('This is a subpage').classes('text-h5 mx-auto mt-24')
    ui.link('Navigate to the index page.', '/').classes('text-lg mx-auto')
    ui.button('back', on_click=lambda: ui.navigate.to('/')).classes('mx-auto')


@ui.page('/')
def index():
    with ui.card().classes('mx-auto p-24 items-center text-center'):
        ui.label('This demonstrates hosting of a NiceGUI app on a subpath.').classes('text-h5')
        ui.label('As you can see the entire app is available below "/nicegui".').classes('text-lg')
        ui.label('But the code here does not need to know that.').classes('text-lg')
        ui.link('Navigate to a subpage.', 'subpage').classes('text-lg')


ui.run()
