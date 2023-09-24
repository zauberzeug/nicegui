import logging
import os
from typing import Any, Callable, Dict

from descope import AuthException, DescopeClient

from nicegui import Client, app, ui

descope_id = os.environ.get('DESCOPE_ID', '')

try:
    descope_client = DescopeClient(project_id=descope_id)
except Exception as error:
    logging.exception("failed to initialize.")


def login_form():
    with ui.card().classes('w-96 mx-auto'):
        return ui.element('descope-wc').props(f'project-id="{descope_id}" flow-id="sign-up-or-in"') \
            .on('success', lambda e: app.storage.user.update({'descope': e.args['detail']['user']}))


def about() -> Dict[str, Any]:
    try:
        return app.storage.user['descope']
    except AuthException:
        logging.exception("Unable to load user.")
        return {}


async def logout():
    result = await ui.run_javascript('return await sdk.logout()', respond=True)
    if result['code'] != 200:
        logging.error('Logout failed: ' + result)
        ui.notify('Logout failed', type='negative')
    else:
        app.storage.user['descope'] = None
    ui.open('/login')


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
            if token and self._verify(token):
                if self.path == '/login':
                    self.refresh_token()
                    ui.open('/')
                else:
                    func()
            else:
                if self.path != '/login':
                    ui.open('/login')
                else:
                    ui.timer(30, self.refresh_token)
                    func()

        return super().__call__(content)

    @staticmethod
    def _verify(token: str):
        try:
            descope_client.validate_session(session_token=token)
            return True
        except AuthException:
            logging.exception("Could not validate user session.")
            ui.notify('Wrong username or password', type='negative')
            return False

    @staticmethod
    async def refresh_token():
        await ui.run_javascript('sdk.refresh()', respond=False)


def login_page(func: Callable[..., Any]) -> Callable[..., Any]:
    return page('/login')(func)
