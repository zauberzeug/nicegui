#!/usr/bin/env python3
from io import StringIO
from uuid import uuid4

from fastapi.responses import StreamingResponse

from nicegui import Client, app, ui


@ui.page('/')
async def index(client: Client):
    download_path = f"/download/{uuid4()}.txt"

    @app.get(download_path)
    async def download():
        # create a file-like object from the string
        string_io = StringIO(text_entry.value)
        return StreamingResponse(
            string_io, media_type="text/plain",
            headers={'Content-Disposition': 'attachment; filename=download.txt', }
        )

    text_entry = ui.textarea(value="hello world")
    ui.button("Download", on_click=lambda: ui.download(download_path))
    # cleanup the download route after the client disconnected
    await client.disconnected()
    app.routes[:] = [route for route in app.routes if route.path != download_path]

ui.run()
