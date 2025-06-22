from typing import Callable

from nicegui import app, ui
from nicegui.elements.sub_pages import SubPages, find_child_sub_pages_element


def protected(func: Callable) -> Callable:
    """Decorator to mark a route handler as requiring authentication for the custom_sub_pages."""
    func._is_protected = True  # pylint: disable=protected-access
    return func


class CustomSubPages(SubPages):
    """Custom ui.sub_pages with built-in authentication and custom 404 handling."""

    def show(self, full_path: str) -> None:
        match_result = self.find_route_match(full_path)
        if match_result is not None:
            if self._is_route_protected(match_result.builder):
                if not self._is_authenticated():
                    self._show_login_form(full_path)
                    return
            self._replace_content(match_result)
            child_sub_pages = find_child_sub_pages_element(self)
            if child_sub_pages:
                child_sub_pages.show(full_path[len(match_result.path):])
            return
        self._show_404_page(full_path)

    def _is_route_protected(self, handler: Callable) -> bool:
        return getattr(handler, '_is_protected', False)

    def _is_authenticated(self) -> bool:
        return app.storage.user.get('authenticated', False)

    def _show_login_form(self, intended_path: str) -> None:
        self.clear()
        with self:
            with ui.card().classes('absolute-center'):
                ui.label('Protected Area').classes('text-xl mb-4')
                ui.label('Enter passphrase to continue:').classes('mb-2')
                passphrase_input = ui.input('Passphrase', password=True, password_toggle_button=True) \
                    .classes('w-64')

                def try_login():
                    if passphrase_input.value == 'spa':
                        app.storage.user['authenticated'] = True
                        ui.navigate.to(intended_path)
                    else:
                        ui.notify('Incorrect passphrase', color='negative')
                        passphrase_input.value = ''

                passphrase_input.on('keydown.enter', try_login)
                ui.button('Login', on_click=try_login).classes('w-full mt-2')

    def _show_404_page(self, path: str) -> None:
        self.clear()
        with self:
            with ui.column().classes('items-center text-center p-8'):
                ui.icon('error_outline', size='4rem').classes('text-red-500 mb-4')
                ui.label('404 - Page Not Found').classes('text-3xl text-red-500 mb-2')
                ui.label(f'The page "{path}" does not exist.').classes('text-gray-600 mb-4')
                ui.separator().classes('w-32 mb-4')
                with ui.row().classes('gap-4'):
                    ui.button('Go Home', on_click=lambda: ui.navigate.to('/')).props('outline')
                    ui.button('Go Back', on_click='history.back()').props('outline')


# Function-like access following NiceGUI convention where classes are callable to feel like functions
custom_sub_pages = CustomSubPages
