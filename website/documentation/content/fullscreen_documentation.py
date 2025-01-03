from nicegui import ui

from . import doc


@doc.demo(ui.app_fullscreen)
def main_demo() -> None:
    fs = ui.app_fullscreen()
    
    with ui.card().classes('w-full items-center'):
        ui.label('Try fullscreen mode!')
        with ui.row():
            ui.button('Enter Fullscreen', on_click=fs.enter)
            ui.button('Exit Fullscreen', on_click=fs.exit)
            ui.button('Toggle Fullscreen', on_click=fs.toggle)


@doc.demo('Requiring long-press to exit', '''
    You can require users to long-press the escape key to exit fullscreen mode.
    This is useful to prevent accidental exits, for example when working on forms or editing data.

    Note that this feature only works in some browsers like Google Chrome or Microsoft Edge.
''')
def toggle_demo():
    fs = ui.app_fullscreen()
    with ui.card().classes('w-full items-center'):
        ui.label('Toggle fullscreen with optional long-press escape')
        with ui.row():
            ui.switch('Require escape hold').bind_value_to(fs, 'require_escape_hold')
            ui.button('Toggle Fullscreen', on_click=lambda: fs.toggle())


@doc.demo('Tracking fullscreen state', '''
    You can track when the fullscreen state changes.

    Note that due to security reasons, fullscreen mode can only be entered from a previous user interaction
    such as a button click.
''')
def state_demo():
    def state_change(e):
        ui.notify(f'Fullscreen {"enabled" if e.value else "disabled"}')
        update_state()
    
    def update_state():
        state = fs.state
        label.text = f'Fullscreen: {"Yes" if state else "No"}'
    
    fs = ui.app_fullscreen(on_state_change=state_change)
    label = ui.label()
    update_state()

    with ui.card().classes('w-full items-center'):
        ui.button('Toggle Fullscreen', on_click=fs.toggle)
        label


doc.reference(ui.app_fullscreen)
