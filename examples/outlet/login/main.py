from nicegui import ui


@ui.outlet('/')
def main_router(url_path: str):
    with ui.header():
        with ui.link('', '/').style('text-decoration: none; color: inherit;') as lnk:
            ui.html('<span style="color:white">Nice</span>'
                    '<span style="color:black">CLOUD</span>').classes('text-h3')


@main_router.view('/')
def main_app_index():
    # login page
    ui.label('Welcome to NiceCLOUD!').classes('text-3xl')
    ui.html('<br>')
    ui.label('Username:')
    ui.textbox('username')
    ui.label('Password:')
    ui.password('password')


ui.run(show=False)
