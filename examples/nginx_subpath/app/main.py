from nicegui import ui


@ui.page('/subpage')
def subpage():
    ui.label('This is a subpage')


@ui.page('/')
def index():
    with ui.card().classes('mx-auto px-24 pt-12 pb-24 items-center'):
        ui.label('this demonstrates hosting of a NiceGUI app on a subpath').classes('text-h5')
        ui.label('as you can see the entire app is available below /nicegui but the code here does not need to know that').classes('text-lg')
        ui.link('navigate to a subpage', subpage).classes('text-lg')


ui.run()
