import logging
import os
from typing import Any, Callable, Dict

from descope import AuthException, DescopeClient

from nicegui import app, helpers, ui

DESCOPE_ID = os.environ.get('DESCOPE_PROJECT_ID', '')

try:
    descope_client = DescopeClient(project_id=DESCOPE_ID)
except AuthException as ex:
    print(ex.error_message)


def login_form() -> ui.element:
    """Create and return the Descope login form."""
    with ui.card().classes('w-96 mx-auto'):
        return ui.element('descope-wc').props(f'project-id="{DESCOPE_ID}" flow-id="sign-up-or-in"') \
            .on('success', lambda e: app.storage.user.update({'descope': e.args['detail']['user']}))


def about() -> Dict[str, Any]:
    """Return the user's Descope profile.

    This function can only be used after the user has logged in.
    """
    return app.storage.user['descope']


async def logout() -> None:
    """Logout the user."""
    result = await ui.run_javascript('return await sdk.logout()')
    if result['code'] == 200:
        app.storage.user['descope'] = None
    else:
        logging.error(f'Logout failed: {result}')
        ui.notify('Logout failed', type='negative')
    ui.navigate.to(page.LOGIN_PATH)


class page(ui.page):
    """A page that requires the user to be logged in.

    It allows the same parameters as ui.page, but adds a login check.
    As recommended by Descope, this is done via JavaScript and allows to use Flows.
    But this means that the page has already awaited the client connection.
    So `ui.add_head_html` will not work.
    """
    SESSION_TOKEN_REFRESH_INTERVAL = 30
    LOGIN_PATH = '/login'

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        async def content():
            ui.add_head_html('<script src="https://unpkg.com/@descope/web-component@latest/dist/index.js"></script>')
            ui.add_head_html('<script src="https://unpkg.com/@descope/web-js-sdk@latest/dist/index.umd.js"></script>')
            ui.add_body_html(f'''
                <script>
                    const sdk = Descope({{ projectId: '{DESCOPE_ID}', persistTokens: true, autoRefresh: true }});
                    const sessionToken = sdk.getSessionToken()
                </script>
            ''')
            await ui.context.client.connected()
            if await self._is_logged_in():
                if self.path == self.LOGIN_PATH:
                    self._refresh()
                    ui.navigate.to('/')
                    return
            else:
                if self.path != self.LOGIN_PATH:
                    ui.navigate.to(self.LOGIN_PATH)
                    return
                ui.timer(self.SESSION_TOKEN_REFRESH_INTERVAL, self._refresh)

            if helpers.is_coroutine_function(func):
                await func()
            else:
                func()

        return super().__call__(content)

    @staticmethod
    async def _is_logged_in() -> bool:
        if not app.storage.user.get('descope'):
            return False
        token = await ui.run_javascript('return sessionToken && !sdk.isJwtExpired(sessionToken) ? sessionToken : null;')
        if not token:
            return False
        try:
            descope_client.validate_session(session_token=token)
            return True
        except AuthException:
            logging.exception('Could not validate user session.')
            ui.notify('Wrong username or password', type='negative')
            return False

    @staticmethod
    def _refresh() -> None:
        ui.run_javascript('sdk.refresh()')


def login_page(func: Callable[..., Any]) -> Callable[..., Any]:
    """Marks the special page that will contain the login form."""
    return page(page.LOGIN_PATH)(func)
