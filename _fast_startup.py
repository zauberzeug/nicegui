import time

start = time.time()
if __name__ == "__main__":
    from nicegui import app, ui


def runme():
    app.shutdown()


if __name__ == "__main__":
    #app.on_startup(runme)
    ui.textarea("Hello!")
    ui.run(
        reload=False,
        show=False,
        native=True,
    )
print(time.time() - start)
