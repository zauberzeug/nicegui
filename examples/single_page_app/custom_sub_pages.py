from typing import Callable

from nicegui import app, ui
from nicegui.page_arguments import RouteMatch


def protected(func: Callable) -> Callable:
    """Decorator to mark a route handler as requiring authentication for the custom_sub_pages."""
    func._is_protected = True  # pylint: disable=protected-access
    return func


class CustomSubPages(ui.sub_pages):
    """Custom ui.sub_pages with built-in authentication and custom 404 handling."""

    def _render_page(self, match: RouteMatch) -> bool:
        if self._is_route_protected(match.builder) and not self._is_authenticated():
            self._show_login_form(match.full_url)
            return True
        return super()._render_page(match)

    def _render_404(self) -> None:
        with ui.column().classes('absolute-center items-center'):
            ui.icon('error_outline', size='4rem').classes('text-red')
            ui.label('404 - Page Not Found').classes('text-2xl text-red')
            ui.label(f'The page "{self._router.current_path}" does not exist.').classes('text-gray-600')
            with ui.row().classes('mt-4'):
                ui.button('Go Home', icon='home', on_click=lambda: ui.navigate.to('/')).props('outline')
                ui.button('Go Back', icon='arrow_back', on_click=ui.navigate.back).props('outline')

    def _render_error(self, error: Exception) -> None:
        with ui.column().classes('absolute-center items-center'):
            ui.icon('error_outline', size='4rem').classes('text-red')
            ui.label('500 - Internal Server Error').classes('text-2xl text-red')
            ui.label(f'The page "{self._router.current_path}" produced an error.').classes('text-gray-600')
            # NOTE: we do not recommend to show exception messages in production (security risk)
            ui.label(str(error)).classes('text-gray-600')
            with ui.row().classes('mt-4'):
                ui.button('Go Home', icon='home', on_click=lambda: ui.navigate.to('/')).props('outline')
                ui.button('Go Back', icon='arrow_back', on_click=ui.navigate.back).props('outline')

    def _is_route_protected(self, handler: Callable) -> bool:
        return getattr(handler, '_is_protected', False)

    def _is_authenticated(self) -> bool:
        return app.storage.user.get('authenticated', False)

    def _show_login_form(self, intended_path: str) -> None:
        with ui.card().classes('absolute-center items-stretch'):
            ui.label('Protected Area').classes('text-2xl')
            ui.label('Enter passphrase to continue.')
            passphrase = ui.input('Passphrase', password=True, password_toggle_button=True) \
                .classes('w-64').props('autofocus')

            def try_login():
                if passphrase.value == 'spa':
                    app.storage.user['authenticated'] = True
                    self._reset_match()  # NOTE: reset the current match to allow the page to be rendered again
                    ui.navigate.to(intended_path)
                else:
                    ui.notify('Incorrect passphrase', color='negative')

            passphrase.on('keydown.enter', try_login)
            ui.button('Login', on_click=try_login)


# Function-like access following NiceGUI convention where classes are callable to feel like functions
custom_sub_pages = CustomSubPages
