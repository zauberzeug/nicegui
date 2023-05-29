#!/usr/bin/env python3
'''This is a just very simple authentication example.

Please see the `OAuth2 example at FastAPI <https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/>`_  or
use the great `Authlib package <https://docs.authlib.org/en/v0.13/client/starlette.html#using-fastapi>`_ to implement a classing real authentication system.
Here we just demonstrate the NiceGUI integration.
'''

from fastapi.responses import RedirectResponse

from nicegui import app, ui

# in reality users passwords would obviously need to be hashed
users = [('user1', 'pass1'), ('user2', 'pass2')]


@ui.page('/')
def main_page() -> None:
    if not app.storage.individual.get('authenticated', False):
        return RedirectResponse('/login')
    with ui.column().classes('absolute-center items-center'):
        ui.label(f'Hello {app.storage.individual["username"]}!').classes('text-2xl')
        ui.button('', on_click=lambda: (app.storage.individual.clear(), ui.open('/login'))) \
            .props('outline round icon=logout')


@ui.page('/login')
def login() -> None:
    def try_login() -> None:  # local function to avoid passing username and password as arguments
        if (username.value, password.value) in users:
            app.storage.individual.update({'username': username.value, 'authenticated': True})
            ui.open('/')
        else:
            ui.notify('Wrong username or password', color='negative')

    if app.storage.individual.get('authenticated', False):
        return RedirectResponse('/')
    with ui.card().classes('absolute-center'):
        username = ui.input('Username').on('keydown.enter', try_login)
        password = ui.input('Password').props('type=password').on('keydown.enter', try_login)
        ui.button('Log in', on_click=try_login)


ui.run()
