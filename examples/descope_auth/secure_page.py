import logging
import os
from typing import Any, Callable

from descope import REFRESH_SESSION_TOKEN_NAME, SESSION_TOKEN_NAME, AuthException, DeliveryMethod, DescopeClient

from nicegui import Client, app, ui

descope_id = os.environ.get('DESCOPE_ID', '')

try:
    descope_client = DescopeClient(project_id=descope_id)
except Exception as error:
    print("failed to initialize. Error:")
    print(error)


async def logout():
    ic(await ui.run_javascript('return await sdk.logout()', respond=True))
    ui.open('/login')


def verify(token: str):
    try:
        jwt_response = descope_client.validate_session(session_token=token)
        app.storage.user['session_token'] = token
        return True
    except Exception:
        app.storage.user['session_token'] = None
        logging.exception("Could not validate user session.")
        ui.notify('Wrong username or password', type='negative')
        return False


class secure_page(ui.page):

    def __init__(self, path):
        super().__init__(path)

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        async def content(client: Client):
            ui.add_head_html('<script src="https://unpkg.com/@descope/web-component@latest/dist/index.js"></script>')
            ui.add_head_html('<script src="https://unpkg.com/@descope/web-js-sdk@latest/dist/index.umd.js"></script>')
            ui.add_body_html('''
                <script>
                    const sdk = Descope({ projectId: \'''' + descope_id + '''\', persistTokens: true, autoRefresh: true });
                    const sessionToken = sdk.getSessionToken()
                </script>                 
            ''')
            await client.connected()
            token = await ui.run_javascript('return sessionToken && !sdk.isJwtExpired(sessionToken) ? sessionToken : null;')
            if token and verify(token):
                if self.path == '/login':
                    await ui.run_javascript('sdk.refresh()', respond=False)
                    ui.open('/')
                else:
                    func()
            else:
                if self.path != '/login':
                    ui.open('/login')
                else:
                    func()

        return super().__call__(content)
