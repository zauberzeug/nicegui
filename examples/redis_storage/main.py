#! /usr/bin/env python3
from nicegui import app, ui


@ui.page('/')
def index():
    ui.input('general').bind_value(app.storage.general, 'text')
    ui.input('user').bind_value(app.storage.user, 'text')


ui.run(storage_secret='your private key to secure the browser session cookie')
