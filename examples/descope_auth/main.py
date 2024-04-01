#!/usr/bin/env python3
import json

import user

from nicegui import ui


@user.login_page
def login():
    user.login_form().on('success', lambda: ui.navigate.to('/'))


@user.page('/')
def home():
    ui.code(json.dumps(user.about(), indent=2), language='json')
    ui.button('Logout', on_click=user.logout)


@user.page('/async')
async def async_page():
    await ui.button('Wait for it...').clicked()
    ui.label('This is an async page')


ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED')
