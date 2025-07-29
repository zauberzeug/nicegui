#!/usr/bin/env python3
import uvicorn
from fastapi import FastAPI

from nicegui import app, ui

# This example deliberately creates a separate FastAPI app and runs NiceGUI on top of it using `ui.run_with`.
# Please note that the `app` object from NiceGUI is also a FastAPI app.
# Often it is easier to stick to `ui.run` and use the `@app.get` etc. decorators to add normal FastAPI endpoints.
fastapi_app = FastAPI()


@fastapi_app.get('/')
def get_root():
    return {'message': 'Hello, FastAPI! Browse to /gui to see the NiceGUI app.'}


@ui.page('/')
def show():
    ui.label('Hello, NiceGUI!')

    # NOTE dark mode will be persistent for each user across tabs and server restarts
    ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
    ui.checkbox('dark mode').bind_value(app.storage.user, 'dark_mode')


ui.run_with(
    fastapi_app,
    mount_path='/gui',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
    storage_secret='pick your private secret here',  # NOTE setting a secret is optional but allows for persistent storage per user
)

if __name__ == '__main__':
    uvicorn.run('main:fastapi_app', log_level='info', reload=True)
