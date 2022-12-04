#!/usr/bin/env python3
'''This is only a very simple authentication example which stores session ids in memory and does not do any password hashing.

Please see the `OAuth2 example at FastAPI <https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/>`_  or
use the great `Authlib package <https://docs.authlib.org/en/v0.13/client/starlette.html#using-fastapi>`_ to implement a real authentication system.

Here we just demonstrate the NiceGUI integration.
'''

import uuid
from typing import Dict

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from nicegui import app, ui

app.add_middleware(SessionMiddleware, secret_key='some_random_string')  # use your own secret key here

# in reality users and session_info would be persistent (e.g. database, file, ...) and passwords obviously hashed
users = [('user1', 'pass1'), ('user2', 'pass2')]
session_info: Dict[str, Dict] = {}


@ui.page('/')
def main_page(request: Request) -> None:
    if is_authenticated(request):
        session = session_info[request.session['id']]
        with ui.row().classes('absolute-center'):
            ui.label(f'Hello {session["username"]}!').classes('text-2xl')
    else:
        return RedirectResponse('/login')


@ui.page('/login')
def login(request: Request) -> None:
    if is_authenticated(request):
        return RedirectResponse('/')
    request.session['id'] = str(uuid.uuid4())  # NOTE this stores a new session id in the cookie of the client
    with ui.card().classes('absolute-center'):
        username = ui.input('Username')
        password = ui.input('Password').classes('w-full').props('type=password')
        ui.button('Log in', on_click=lambda: try_login(request.session['id'], username.value, password.value))


def is_authenticated(request: Request) -> bool:
    return session_info.get(request.session.get('id'), {}).get('authenticated', False)


def try_login(session_id: str, username: str, password: str) -> None:
    if (username, password) in users:
        session_info[session_id] = {'username': username, 'authenticated': True}
    ui.open('/')


ui.run()
