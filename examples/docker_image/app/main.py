import os
import signal

from nicegui import app, ui

signal.signal(signal.SIGINT, app.shutdown)
signal.signal(signal.SIGTERM, app.shutdown)


@ui.page('/')
def index():
    ui.textarea('This note is kept between visits') \
        .classes('w-96').bind_value(app.storage.user, 'note')


def my_shutdown():
    print("Shutdown has been initiated!")


app.on_shutdown(my_shutdown)
ui.run(storage_secret=os.environ['STORAGE_SECRET'])
