from fastapi import FastAPI
from nicegui import ui


def init(app: FastAPI) -> None:
    @ui.page('/show')
    def show():
        ui.label('Hello, FastAPI!')

    ui.run_with(app)
