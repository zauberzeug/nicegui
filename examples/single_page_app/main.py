#!/usr/bin/env python3
from custom_sub_pages import custom_sub_pages, protected

from nicegui import app, ui


@ui.page('/')
@ui.page('/{_:path}')
def main_page():
    with ui.header().classes('justify-between items-center p-4 bg-blue-100'):
        with ui.row().classes('gap-2'):
            ui.button('Home', on_click=lambda: ui.navigate.to('/')).props('flat')
            ui.button('Admin', on_click=lambda: ui.navigate.to('/admin')).props('flat')
            ui.button('Secret', on_click=lambda: ui.navigate.to('/secret')).props('flat')
            ui.button('Invalid', on_click=lambda: ui.navigate.to('/invalid')).props('flat')

        with ui.row().classes('items-center gap-2').bind_visibility_from(app.storage.user, 'authenticated'):
            ui.icon('lock_open').classes('text-green-600')
            ui.label('Authenticated').classes('text-green-600 text-sm')
            ui.button('Logout', on_click=lambda: [
                app.storage.user.update(authenticated=False),
                ui.navigate.to('/')
            ]).props('flat')

    custom_sub_pages({
        '/': show_home,
        '/admin': show_admin,
        '/secret': show_secret,
    }).classes('flex-grow p-4')


def show_home():
    ui.markdown('''
        This example shows inheritance from `ui.sub_pages` for decorator-based route protection and a custom 404 page.

        **Try it:** Navigate to Admin/Secret pages (passphrase: "spa") or Invalid for 404.
    ''')


@protected
def show_admin():
    ui.label('Admin Dashboard').classes('text-2xl mb-4')
    ui.icon('admin_panel_settings', size='2rem').classes('text-blue-600 mb-2')
    ui.label('You have successfully accessed the protected admin area!').classes('text-green-600')


@protected
def show_secret():
    ui.label('Secret Area').classes('text-2xl mb-4')
    ui.icon('lock', size='2rem').classes('text-purple-600 mb-2')
    ui.label('This is confidential information only for authenticated users.').classes('text-purple-600')


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(storage_secret='demo_secret_key_change_in_production')
