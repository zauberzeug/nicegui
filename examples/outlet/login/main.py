import html
import uuid
from typing import Optional

from nicegui import ui, app
from nicegui.single_page_target import SinglePageTarget

INDEX_URL = '/'
SECRET_AREA_URL = '/secret_area'

DUMMY_LOGINS = {"admin": "NicePass"}


def portal_rerouting(url) -> str:
    # automatically redirect to the secret area if the user is already logged in
    if '/' == INDEX_URL:
        if 'login_token' in app.storage.tab:
            return SECRET_AREA_URL
    return url


@ui.outlet('/', on_navigate=portal_rerouting)
def main_router():
    with ui.header():
        with ui.link('', '/').style('text-decoration: none; color: inherit;') as lnk:
            ui.html('<span style="color:white">Nice</span>'
                    '<span style="color:black">CLOUD</span>').classes('text-h3')
    with ui.element() as border:
        border.style('margin: 20pt;')
        yield


@main_router.view('/', title='🚪 NiceCLOUD Login')
def main_app_index():
    def handle_login():
        username = input_field.value
        password = pw.value
        inv_pw.clear()
        if username in DUMMY_LOGINS and DUMMY_LOGINS[username] == password:
            app.storage.tab['login_token'] = uuid.uuid4().hex
            app.storage.tab['username'] = username
            ui.navigate.to(SECRET_AREA_URL)
        else:
            with inv_pw:
                ui.label('Invalid password!').style('color: red;')

    # login page
    with ui.column() as col:
        ui.label('Login to NiceCLOUD!').classes('text-3xl')
        ui.html('<br>')
        input_field = ui.input('Username').style('width: 100%').on('keydown.enter', lambda: pw.focus())
        pw = ui.input('Password', password=True,
                      password_toggle_button=True).style('width: 100%').on('keydown.enter', handle_login)
        col.style('width: 300pt; top: 40%; left: 50%; transform: translate(-50%, -50%); position: absolute;')
        # horizontally centered button
        with ui.row().style('justify-content: center;'):
            ui.button('Login').style('width: 100pt; left: 50%; '
                                     'transform: translate(-50%, 0); position: absolute;').on_click(handle_login)
        inv_pw = ui.row()
        # give user and password hint
        ui.html('<br>')
        ui.label('Hint: admin/NicePass').style('color: gray;')
        # provide link to try to access secret page w/o login
        ui.html('<br>')
        ui.link('Try to access secret area without login', SECRET_AREA_URL).style('color: gray;')


def logout():  # logs the user out and redirects to the login page
    del app.storage.tab['login_token']
    app.storage.tab.clear()
    ui.navigate.to(INDEX_URL)


def check_login(url) -> Optional[SinglePageTarget]:
    def error_page():
        with ui.column().style('align-items: center; justify-content: center; left: 50%; top: 50%; '
                               'transform: translate(-50%, -50%); position: absolute;'):
            ui.label('⚠️').classes('text-6xl')
            ui.label('You are not logged in!').classes('text-3xl')
            ui.html('<br>')
            ui.button('🚪 Go to login page').on_click(lambda: ui.navigate.to(INDEX_URL)).style('width: 200pt;')

    if 'login_token' not in app.storage.tab:  # check if the user is not logged in
        return SinglePageTarget(url, builder=error_page, title='Not logged in')
    return None  # default behavior


@main_router.outlet(SECRET_AREA_URL, on_resolve=check_login)
def secret_area_router():
    yield


@secret_area_router.view('/', title='🔒 Secret Area')
def secret_area_index():
    with ui.column():
        user_name = app.storage.tab['username']
        esc_name = html.escape(user_name)
        ui.html(f'Welcome to the secret area <b>{esc_name}</b>!<br><br>').classes('text-3xl')
        ui.html('You chose the right place, we have cookies! 🍪<br><br>').classes('text-2xl')
        ui.button('Logout').on_click(logout)


ui.run(show=False, storage_secret='secret', title='NiceCLOUD')
