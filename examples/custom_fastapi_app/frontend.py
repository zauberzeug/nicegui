from fastapi import FastAPI


def init(app: FastAPI) -> None:
    import builtins
    builtins.nicegui_APP = app
    from nicegui import ui, globals

    @ui.page('/show')
    def show():
        ui.label('Hello World, FastAPI!')

    globals.title = 'FastAPI'
    globals.favicon = None
    globals.dark = False
    globals.binding_refresh_interval = 0.1
    globals.excludes = []
    globals.host = 'localhost'
    globals.port = 8000
