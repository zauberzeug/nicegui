#!/usr/bin/env python3

import logging
import os

from descope import REFRESH_SESSION_TOKEN_NAME, SESSION_TOKEN_NAME, AuthException, DeliveryMethod, DescopeClient
from fastapi import Request
from fastapi.responses import RedirectResponse
from icecream import ic
from starlette.middleware.base import BaseHTTPMiddleware

import nicegui.globals
from nicegui import Client, app, events, ui

descope_id = os.environ.get('DESCOPE_ID', '')
try:
    descope_client = DescopeClient(project_id=descope_id)
except Exception as error:
    print("failed to initialize. Error:")
    print(error)


def validate_session():
    return
    # Fetch session token from HTTP Authorization Header
    session_token = "xxxx"

    try:
        jwt_response = descope_client.validate_session(session_token=session_token)
        print("Successfully validated user session:")
        print(jwt_response)
    except Exception:
        logging.exception("Could not validate user session.")


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if request.url.path in nicegui.globals.page_routes.values() and request.url.path not in unrestricted_page_routes:
                app.storage.user['referrer_path'] = request.url.path  # remember where the user wanted to go
                return RedirectResponse('/login')
        return await call_next(request)


app.add_middleware(AuthMiddleware)

unrestricted_page_routes = {'/login'}


def verify(token: str):
    ic()
    try:
        jwt_response = descope_client.validate_session(session_token=token)
        ic(jwt_response)
        return True
    except Exception:
        logging.exception("Could not validate user session.")
        ui.notify('Wrong username or password', type='negative')
        return False


@ui.page('/login')
async def login(client: Client):
    ui.add_head_html('<script src="https://unpkg.com/@descope/web-js-sdk/dist/index.umd.js"></script>')
    ui.add_body_html('''
        <script>
            const sdk = Descope({ projectId: \'''' + descope_id + '''\', persistTokens: true, autoRefresh: true });
            const sessionToken = sdk.getSessionToken()
        </script>                 
    ''')

    await client.connected()
    token = await ui.run_javascript('''
            if (sessionToken && !sdk.isJwtExpired(sessionToken)) {
                return sessionToken;
            } else {
                return null;
            }
    ''')
    with ui.card().classes('w-96 mx-auto'):
        if token and verify(token):
            app.storage.user['authenticated'] = True
            ui.open('/')
        else:
            ui.add_head_html('<script src="https://unpkg.com/@descope/web-component/dist/index.js"></script>')
            ui.element('descope-wc').props(f'project-id="{descope_id}" flow-id="sign-up-or-in"') \
                .on('success', lambda: ui.open('/'))


@ui.page('/')
def home():
    ui.add_body_html('''
        <script src="https://unpkg.com/@descope/web-js-sdk/dist/index.umd.js"></script>
        <script>
            sdk.refresh()
        </script>                 
    ''')

    ui.label('Welcome!')


ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED')
