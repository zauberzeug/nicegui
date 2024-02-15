#!/usr/bin/env python3
import io
import uuid

from fastapi.responses import StreamingResponse

from nicegui import Client, app, ui


@ui.page('/')
async def index(client: Client):
    """
    This function defines the index route of the web application.
    It allows the user to download a text file containing the content of a textarea.

    Parameters:
    - client (Client): The client object representing the connected client.

    Returns:
    - None

    Usage:
    1. Call this function with the connected client object as the argument.
    2. The function sets up a download route for the text file.
    3. The user can enter text in a textarea.
    4. Clicking the "Download" button will trigger the download of a text file containing the textarea content.
    5. The download route is cleaned up after the client disconnects.
    """
    download_path = f'/download/{uuid.uuid4()}.txt'

    @app.get(download_path)
    def download():
        """
        This function defines the download route for the text file.

        Returns:
        - StreamingResponse: The streaming response object representing the text file download.

        Usage:
        - This function is called automatically when the download route is accessed.
        - It creates a file-like object from the content of the textarea.
        - The file is returned as a streaming response with the appropriate headers.
        """
        string_io = io.StringIO(textarea.value)  # create a file-like object from the string
        headers = {'Content-Disposition': 'attachment; filename=download.txt'}
        return StreamingResponse(string_io, media_type='text/plain', headers=headers)

    textarea = ui.textarea(value='Hello World!')
    ui.button('Download', on_click=lambda: ui.download(download_path))

    # cleanup the download route after the client disconnected
    await client.disconnected()
    app.routes[:] = [route for route in app.routes if route.path != download_path]

ui.run()
