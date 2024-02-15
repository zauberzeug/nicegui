import logging
import os
from typing import Any, Callable, Dict

from descope import AuthException, DescopeClient

from nicegui import Client, app, helpers, ui

DESCOPE_ID = os.environ.get('DESCOPE_PROJECT_ID', '')

try:
    descope_client = DescopeClient(project_id=DESCOPE_ID)
except AuthException as ex:
    print(ex.error_message)


def login_form() -> ui.element:
    """
    Create and return the Descope login form.

    This function creates a login form using the NiceGUI library and returns it as a UI element.
    The login form is designed for the Descope application and allows users to sign up or sign in.
    The form is wrapped inside a card element with a width of 96 pixels and centered horizontally.

    Returns:
        ui.element: The Descope login form as a UI element.

    Example usage:
        form = login_form()
        # Add the form to a parent UI element or render it to the screen
    """
    with ui.card().classes('w-96 mx-auto'):
        return ui.element('descope-wc').props(f'project-id="{DESCOPE_ID}" flow-id="sign-up-or-in"') \
            .on('success', lambda e: app.storage.user.update({'descope': e.args['detail']['user']}))


def about() -> Dict[str, Any]:
    """
    Return the user's Descope profile.

    This function retrieves the user's Descope profile from the app's storage.
    It can only be used after the user has logged in.

    Returns:
        A dictionary containing the user's Descope profile.

    Raises:
        KeyError: If the user's Descope profile is not found in the app's storage.

    Example:
        >>> profile = about()
        >>> print(profile)
        {'name': 'John Doe', 'email': 'johndoe@example.com', 'age': 30}
    """
    return app.storage.user['descope']

async def logout() -> None:
    """Logout the user.

    This function logs out the user by calling the `sdk.logout()` JavaScript function
    and updating the user's `descope` attribute in the app's storage.

    Returns:
        None

    Raises:
        None

    Usage:
        Call this function to log out the user. It will execute the `sdk.logout()` JavaScript
        function and update the user's `descope` attribute in the app's storage. If the logout
        is successful, the user will be redirected to the login page. If the logout fails, an
        error message will be logged and a notification will be displayed to the user.

    Example:
        await logout()
    """
    result = await ui.run_javascript('return await sdk.logout()')
    if result['code'] == 200:
        app.storage.user['descope'] = None
    else:
        logging.error(f'Logout failed: {result}')
        ui.notify('Logout failed', type='negative')
    ui.open(page.LOGIN_PATH)


class page(ui.page):
    """A page that requires the user to be logged in.

    This class represents a page that requires the user to be logged in to access its content.
    It extends the `ui.page` class and adds a login check functionality.
    The login check is performed using JavaScript and the Descope library, allowing the use of Flows.

    Attributes:
        SESSION_TOKEN_REFRESH_INTERVAL (int): The interval in seconds for refreshing the session token.
        LOGIN_PATH (str): The path for the login page.

    Methods:
        __call__(func: Callable[..., Any]) -> Callable[..., Any]: Decorator method that wraps the content of the page.
        _is_logged_in() -> bool: Checks if the user is logged in.
        _refresh() -> None: Refreshes the session token.

    Usage:
        1. Create an instance of the `page` class, passing the necessary parameters.
        2. Decorate the content function with the `__call__` method of the `page` instance.
        3. Implement the content function, which will be executed when the page is accessed.
        4. Use the `ui.add_head_html` and `ui.add_body_html` methods to add necessary JavaScript code.
        5. Use the `ui.open` method to redirect to other pages.
        6. Use the `ui.timer` method to schedule the session token refresh.
        7. Use the `ui.run_javascript` method to execute JavaScript code.
    """
    SESSION_TOKEN_REFRESH_INTERVAL = 30
    LOGIN_PATH = '/login'

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator that wraps a function with Descope authentication logic.

        This decorator is used to add Descope authentication logic to a function.
        It ensures that the user is authenticated before executing the function,
        and redirects to the login page if the user is not logged in.

        Args:
            func (Callable[..., Any]): The function to be decorated.

        Returns:
            Callable[..., Any]: The decorated function.

        Usage:
            @__call__
            def my_function():
                # Function logic goes here

        Example:
            @__call__
            def my_function():
                if user.is_authenticated():
                    # Perform authenticated actions
                else:
                    # Redirect to login page

        """
        async def content(client: Client):
            ui.add_head_html('<script src="https://unpkg.com/@descope/web-component@latest/dist/index.js"></script>')
            ui.add_head_html('<script src="https://unpkg.com/@descope/web-js-sdk@latest/dist/index.umd.js"></script>')
            ui.add_body_html(f'''
                <script>
                    const sdk = Descope({{ projectId: '{DESCOPE_ID}', persistTokens: true, autoRefresh: true }});
                    const sessionToken = sdk.getSessionToken()
                </script>                 
            ''')
            await client.connected()
            if await self._is_logged_in():
                if self.path == self.LOGIN_PATH:
                    self._refresh()
                    ui.open('/')
                    return
            else:
                if self.path != self.LOGIN_PATH:
                    ui.open(self.LOGIN_PATH)
                    return
                ui.timer(self.SESSION_TOKEN_REFRESH_INTERVAL, self._refresh)

            if helpers.is_coroutine_function(func):
                await func()
            else:
                func()

        return super().__call__(content)

    @staticmethod
    async def _is_logged_in() -> bool:
            """
            Check if the user is logged in.

            This function checks if the user is logged in by validating the session token.
            It first checks if the 'descope' key exists in the user storage. If not, it returns False.
            Then, it retrieves the session token from the UI using JavaScript and checks if it is valid.
            If the token is valid, it attempts to validate the session using the 'descope_client' object.
            If the session validation fails, an AuthException is raised and False is returned.
            If the session validation succeeds, True is returned.

            Returns:
                bool: True if the user is logged in, False otherwise.
            """
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
        """
        Refreshes the user interface by running the 'sdk.refresh()' JavaScript function.

        This function is responsible for updating the user interface to reflect any changes made to the underlying data.
        It should be called whenever there is a need to refresh the UI after performing any relevant operations.

        Returns:
            None
        """
        ui.run_javascript('sdk.refresh()')


def login_page(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator function that marks the special page that will contain the login form.

    Parameters:
    - func: The function to be decorated.

    Returns:
    - The decorated function.

    Usage:
    @login_page
    def my_login_page():
        # Code for the login page goes here
        pass

    The `login_page` decorator is used to mark a function as the special page that will contain the login form.
    This decorator can be applied to any function that represents a web page in an application.

    Example:
    @login_page
    def my_login_page():
        # Code for the login page goes here
        pass

    In the above example, the `my_login_page` function is decorated with `@login_page` to mark it as the login page.
    """
    return page(page.LOGIN_PATH)(func)
