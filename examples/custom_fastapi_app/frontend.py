from fastapi import FastAPI
from nicegui import globals, ui


def init(app: FastAPI) -> None:
    @ui.page('/show')
    def show():
        ui.label('Hello, FastAPI!')

    globals.title = 'FastAPI'
    globals.favicon = None
    globals.dark = False
    globals.binding_refresh_interval = 0.1
    globals.excludes = []
    globals.host = 'localhost'
    globals.port = 8000

    app.mount('/', globals.app)
