import time

start = time.time()

from nicegui import app, ui


def runme():
    app.shutdown()

app.on_startup(runme)
ui.textarea("Hello!")
ui.run(
    reload=False,
    show=False,
    native=True,
)
print(time.time() - start)