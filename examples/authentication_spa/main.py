#!/usr/bin/env python3
import html
import uuid
from typing import Optional, Union

from nicegui import app, ui
from nicegui.single_page_target import SinglePageTarget

INDEX_URL = '/'
SECRET_AREA_URL = '/secret_area'

DUMMY_LOGINS = {"admin": "NicePass"}


def portal_rerouting(url) -> str:
    # automatically redirect to the secret area if the user is already logged in
    if 'login_token' in app.storage.user:
        return SECRET_AREA_URL
    return url


@ui.outlet('/', on_navigate=portal_rerouting)
def main_layout():
    with ui.header():
        ui.link('SPA Login Example', '/').style('text-decoration: none; color: inherit;').classes('text-h3')
    ui.query('.nicegui-content').classes('flex-center')
    with ui.column().classes('m-12'):
        yield


@main_layout.view('/', title='Login Page')
def main_app_index():
    def handle_login():
        username = username_input.value
        password = password_input.value
        if username in DUMMY_LOGINS and DUMMY_LOGINS[username] == password:
            # NOTE you can also use app.storage.tab to ensure the login is only valid for the current tab
            app.storage.user['login_token'] = uuid.uuid4().hex
            app.storage.user['username'] = username
            ui.navigate.to(SECRET_AREA_URL)
        else:
            password_input.props('error')

    with ui.column().classes('w-96 mt-[40%] items-center'):
        username_input = ui.input('Username').classes('w-full')\
            .on('keydown.enter', lambda: password_input.run_method('focus'))
        password_input = ui.input('Password', password=True, password_toggle_button=True) \
            .classes('w-full').props('error-message="Invalid password!"') \
            .on('keydown.enter', handle_login)
        ui.button('Login').classes('w-48').on_click(handle_login)
        ui.label(f'Hint: {DUMMY_LOGINS}').classes('text-grey mt-12')
        ui.link('Try to access secret area without login', SECRET_AREA_URL).classes('text-grey mt-12')


def logout():  # logs the user out and redirects to the login page
    del app.storage.user['login_token']
    ui.navigate.to(INDEX_URL)


def check_login(url) -> Optional[Union[str, SinglePageTarget]]:
    def error_page():
        with ui.column().classes('w-96 mt-[40%] items-center'):
            ui.label('⚠️').classes('text-6xl')
            ui.label('You are not logged in!').classes('text-3xl')
            ui.button('Go to login page').on_click(lambda: ui.navigate.to(INDEX_URL)).classes('w-48 mt-12')

    if 'login_token' not in app.storage.user:  # check if the user is not logged in
        return SinglePageTarget(url, builder=error_page, title='Not logged in')
    return url  # default behavior


@main_layout.outlet(SECRET_AREA_URL, on_navigate=check_login)
def secret_area_layout():
    yield


@secret_area_layout.view('/', title='🔒 Secret Area')
def secret_area_index():
    username = app.storage.user['username']
    ui.label(f'Hello {html.escape(username)}. Welcome to the secret area!').classes('text-3xl')
    ui.button('Logout').on_click(logout).classes('w-48 mt-12')


ui.run(storage_secret='secret', title='SPA Login')
