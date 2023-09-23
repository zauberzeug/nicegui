#!/usr/bin/env python3

import os

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

import nicegui.globals
from nicegui import app, ui


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


@ui.page('/login')
def login():
    ui.add_head_html('''
        <script src="https://unpkg.com/@descope/web-component/dist/index.js"></script>
        <script src="https://unpkg.com/@descope/web-js-sdk/dist/index.umd.js"></script>               
    ''')

    descope_id = os.environ.get('DESCOPE_ID', '')
    with ui.card().classes('w-96 mx-auto') as login_card:
        ui.element('descope-wc').props(f'project-id="{descope_id}" flow-id="sign-up-or-in"')
    login_card.on('success', lambda e: ui.notify('Yes'))
    login_card.on('error', lambda e: ui.notify('No'))
    ui.add_body_html('''
        <script>
            document.addEventListener("DOMContentLoaded", () => {
                const sdk = Descope({ projectId: \'''' + descope_id + '''\', persistTokens: true, autoRefresh: true });

                const sessionToken = sdk.getSessionToken()
                var notValidToken
                if (sessionToken) {
                    notValidToken = sdk.isJwtExpired(sessionToken)
                }
                if (!sessionToken || notValidToken) {
                    var loginElement = getElement(''' + str(login_card.id) + ''');
                    const onSuccess = (e) => {
                        sdk.refresh(),
                        loginElement.$emit('success', encodeURIComponent(e.detail.user.loginIds));
                    };
                    const onError = (err) => loginElement.$emit('error');
                    const wcElement = document.getElementsByTagName('descope-wc')[0];
                    wcElement.addEventListener('success', onSuccess);
                    wcElement.addEventListener('error', onError);
                }
            });
        </script>                 
    ''')


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
