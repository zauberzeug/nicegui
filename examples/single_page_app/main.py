#!/usr/bin/env python3
from custom_sub_pages import custom_sub_pages, protected

from nicegui import app, ui


@ui.page('/')
@ui.page('/{_:path}')
def main_page():
    with ui.header().classes('items-center bg-blue-100'):
        ui.button('Home', on_click=lambda: ui.navigate.to('/')).props('flat')
        ui.button('Secret', on_click=lambda: ui.navigate.to('/secret')).props('flat')
        ui.button('Invalid', on_click=lambda: ui.navigate.to('/invalid')).props('flat')
        ui.button('Error', on_click=lambda: ui.navigate.to('/error')).props('flat')
        ui.space()
        ui.button('Logout', icon='logout').props('flat') \
            .bind_visibility_from(app.storage.user, 'authenticated') \
            .on_click(lambda: app.storage.user.update(authenticated=False)) \
            .on_click(lambda: ui.navigate.to('/'))

    custom_sub_pages({
        '/': home,
        '/secret': secret,
        '/error': error,
    }).classes('flex-grow p-4')


def home():
    ui.markdown('''
        This example shows inheritance from `ui.sub_pages` for decorator-based route protection and a custom 404 page.

        **Try it:** Navigate to "Secret" (passphrase: "spa") or "Invalid" for 404.
    ''')


def error():
    raise ValueError('some error message')


@protected
def secret():
    ui.markdown('''
        ### Secret Area 🔑

        This is confidential information only for authenticated users.
    ''')


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(storage_secret='demo_secret_key_change_in_production')
