#!/usr/bin/env python3

import icecream
import user

from nicegui import ui

icecream.install()


@user.login_page
def login():
    user.login_form().on('success', lambda: ui.open('/'))


@user.page('/')
def home():
    ui.label('Welcome!')
    ui.button('Logout', on_click=user.logout)


ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED')
