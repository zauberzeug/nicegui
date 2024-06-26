#!/usr/bin/env python3
import io
import uuid

from fastapi.responses import StreamingResponse

from nicegui import app, ui


@ui.page('/')
async def index():
    download_path = f'/download/{uuid.uuid4()}.txt'

    @app.get(download_path)
    def download():
        string_io = io.StringIO(textarea.value)  # create a file-like object from the string
        headers = {'Content-Disposition': 'attachment; filename=download.txt'}
        return StreamingResponse(string_io, media_type='text/plain', headers=headers)

    textarea = ui.textarea(value='Hello World!')
    ui.button('Download', on_click=lambda: ui.download(download_path))

    # cleanup the download route after the client disconnected
    await ui.context.client.disconnected()
    app.routes[:] = [route for route in app.routes if route.path != download_path]

ui.run()
