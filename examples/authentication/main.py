#!/usr/bin/env python3
import uuid
from typing import Dict

from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

from nicegui import app, ui

app.add_middleware(SessionMiddleware, secret_key='some_random_string')

session_info: Dict[str, Dict] = {}  # in reality in a database


@ui.page('/')
def main_page(request: Request) -> None:
    if is_authenticated(request):
        create_welcome_message(session_info[request.session['id']]['username'])
    else:
        request.session['id'] = str(uuid.uuid4())
        create_login_form(request.session['id'])


def is_authenticated(request: Request) -> bool:
    return session_info.get(request.session.get('id'), {}).get('authenticated', False)


def create_login_form(session_id: str) -> None:
    with ui.card().classes('absolute-center'):
        username = ui.input('Username')
        password = ui.input('Password').classes('w-full').props('type=password')
        ui.button('Log in', on_click=lambda: try_login(session_id, username.value, password.value))


def try_login(session_id: str, username: str, password: str) -> None:
    if (username, password) in [('user1', 'pass1'), ('user2', 'pass2')]:
        session_info[session_id] = {'username': username, 'authenticated': True}
    ui.open('/')


def create_welcome_message(username: str) -> None:
    with ui.row().classes('absolute-center'):
        ui.label(f'Hello {username}!').classes('text-2xl')


ui.run()
