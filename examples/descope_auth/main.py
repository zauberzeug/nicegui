#!/usr/bin/env python3
import json

import user

from nicegui import ui


@user.login_page
def login():
    user.login_form().on('success', lambda: ui.open('/'))


@user.page('/')
def home():
    ui.code(json.dumps(user.about(), indent=2), language='json')
    ui.button('Logout', on_click=user.logout)


ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED')
