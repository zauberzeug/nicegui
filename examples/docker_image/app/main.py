import os

from nicegui import app, ui


@ui.page('/')
def index():
    ui.textarea('This note is kept between visits') \
        .classes('w-96').bind_value(app.storage.user, 'note')


def handle_shutdown():
    print('Shutdown has been initiated!')


app.on_shutdown(handle_shutdown)
ui.run(storage_secret=os.environ['STORAGE_SECRET'])
