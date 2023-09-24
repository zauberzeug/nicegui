import logging
import os
from typing import Any, Callable, Dict

from descope import AuthException, DescopeClient

from nicegui import Client, app, ui

_descope_id = os.environ.get('DESCOPE_PROJECT_ID', '')

try:
    descope_client = DescopeClient(project_id=_descope_id)
except Exception as error:
    logging.exception("failed to initialize.")


def login_form() -> ui.element:
    """Places and returns the Descope login form."""
    with ui.card().classes('w-96 mx-auto'):
        return ui.element('descope-wc').props(f'project-id="{_descope_id}" flow-id="sign-up-or-in"') \
            .on('success', lambda e: app.storage.user.update({'descope': e.args['detail']['user']}))


def about() -> Dict[str, Any]:
    """Returns the user's Descope profile."""
    infos = app.storage.user['descope']
    if not infos:
        raise Exception('User is not logged in.')


async def logout() -> None:
    """Logs the user out."""
    result = await ui.run_javascript('return await sdk.logout()', respond=True)
    if result['code'] != 200:
        logging.error(f'Logout failed: {result}')
        ui.notify('Logout failed', type='negative')
    else:
        app.storage.user['descope'] = None
    ui.open('/login')


class page(ui.page):

    def __init__(self, path):
        """A page that requires the user to be logged in.

        It allows the same parameters as ui.page, but adds a login check.
        As recommended by Descope this is done via JavaScript and allows to use Flows.
        But this means that the page has already awaited the client connection.
        So `ui.add_head_html` will not work.
        """
        super().__init__(path)

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        async def content(client: Client):
            ui.add_head_html('<script src="https://unpkg.com/@descope/web-component@latest/dist/index.js"></script>')
            ui.add_head_html('<script src="https://unpkg.com/@descope/web-js-sdk@latest/dist/index.umd.js"></script>')
            ui.add_body_html('''
                <script>
                    const sdk = Descope({ projectId: \'''' + _descope_id + '''\', persistTokens: true, autoRefresh: true });
                    const sessionToken = sdk.getSessionToken()
                </script>                 
            ''')
            await client.connected()
            token = await ui.run_javascript('return sessionToken && !sdk.isJwtExpired(sessionToken) ? sessionToken : null;')
            if token and self._verify(token):
                if self.path == '/login':
                    await self.refresh_token()
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
    def _verify(token: str) -> bool:
        try:
            descope_client.validate_session(session_token=token)
            return True
        except AuthException:
            logging.exception("Could not validate user session.")
            ui.notify('Wrong username or password', type='negative')
            return False

    @staticmethod
    async def refresh_token() -> None:
        await ui.run_javascript('sdk.refresh()', respond=False)


def login_page(func: Callable[..., Any]) -> Callable[..., Any]:
    """Marks the special page that will contain the login form."""
    return page('/login')(func)
