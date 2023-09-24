#!/usr/bin/env python3

import icecream
from secure_page import descope_id, logout, secure_page

from nicegui import ui

icecream.install()


@secure_page('/login')
def login():
    with ui.card().classes('w-96 mx-auto'):
        ui.element('descope-wc').props(f'project-id="{descope_id}" flow-id="sign-up-or-in"') \
            .on('success', lambda: ui.open('/'))


@secure_page('/')
def home():
    ui.label('Welcome!')
    ui.button('Logout', on_click=logout)


ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED')
