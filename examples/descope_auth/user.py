import logging
import os
from typing import Any, Callable

from descope import DescopeClient

from nicegui import Client, app, ui

descope_id = os.environ.get('DESCOPE_ID', '')

try:
    descope_client = DescopeClient(project_id=descope_id)
except Exception as error:
    print("failed to initialize. Error:")
    print(error)


async def logout():
    result = await ui.run_javascript('return await sdk.logout()', respond=True)
    if result['code'] != 200:
        logging.error('Logout failed: ' + result)
        ui.notify('Logout failed', type='negative')
    ui.open('/login')


def _verify(token: str):
    try:
        jwt_response = descope_client.validate_session(session_token=token)
        ic(jwt_response)
        app.storage.user['user_id'] = jwt_response['userId']
        return True
    except Exception:
        app.storage.user['user_id'] = None
        logging.exception("Could not validate user session.")
        ui.notify('Wrong username or password', type='negative')
        return False


def login_form():
    with ui.card().classes('w-96 mx-auto'):
        return ui.element('descope-wc').props(f'project-id="{descope_id}" flow-id="sign-up-or-in"')


class page(ui.page):

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
            if token and _verify(token):
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


def login_page(func: Callable[..., Any]) -> Callable[..., Any]:
    return page('/login')(func)
