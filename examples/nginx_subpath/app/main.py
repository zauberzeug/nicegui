from nicegui import ui


@ui.page('/subpage')
def subpage():
    ui.label('This is a subpage.')


@ui.page('/')
def index():
    with ui.card().classes('mx-auto px-24 pt-12 pb-24 items-center'):
        ui.label('This demonstrates hosting of a NiceGUI app on a subpath.').classes('text-h5')
        ui.label('As you can see the entire app is available below "/nicegui".').classes('text-lg')
        ui.label('But the code here does not need to know that.').classes('text-lg')
        ui.link('Navigate to a subpage.', subpage).classes('text-lg')


ui.run()
