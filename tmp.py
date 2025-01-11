from datetime import timedelta

from nicegui import app, ui

app.storage.max_tab_storage_age = timedelta(minutes=1.2).total_seconds()


@ui.page('/')
def index():
    ui.label(f'Tab storage age: {app.storage.max_tab_storage_age} seconds')


ui.run()
