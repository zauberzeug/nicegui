from nicegui import app, ui
import signal

signal.signal(signal.SIGINT, app.shutdown)
signal.signal(signal.SIGTERM, app.shutdown)


def store_name(input):
    app.storage.general['name'] = input.value


ui.input(label='Name', on_change=lambda i: store_name(i))


def my_shutdown():
    print("Shutdown has been initiated!")


app.on_shutdown(my_shutdown)
ui.run()
