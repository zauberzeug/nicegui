#!/usr/bin/env python3
import base64
import signal
import time

import cv2
import numpy as np
from fastapi import Response

from nicegui import Client, app, core, run, ui

# In case you don't have a webcam, this will provide a black placeholder image.
black_1px = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAA1JREFUGFdjYGBg+A8AAQQBAHAgZQsAAAAASUVORK5CYII='
placeholder = Response(content=base64.b64decode(black_1px.encode('ascii')), media_type='image/png')
# OpenCV is used to access the webcam.
video_capture = cv2.VideoCapture(0)


def convert(frame: np.ndarray) -> bytes:
    """
    Convert a frame from OpenCV format to bytes.

    Parameters:
        frame (np.ndarray): The input frame in OpenCV format.

    Returns:
        bytes: The converted frame in bytes format.

    Raises:
        None

    Example:
        frame = cv2.imread('image.jpg')
        converted_frame = convert(frame)
    """
    _, imencode_image = cv2.imencode('.jpg', frame)
    return imencode_image.tobytes()


@app.get('/video/frame')
# Thanks to FastAPI's `app.get`` it is easy to create a web route which always provides the latest image from OpenCV.
async def grab_video_frame() -> Response:
    """
    Grabs a frame from the video capture and returns it as a JPEG image.

    Returns:
        Response: The response object containing the JPEG image.

    Raises:
        None

    Notes:
        - This function assumes that `video_capture` is a valid and opened video capture object.
        - The `video_capture.read` call is a blocking function, so it is run in a separate thread to avoid blocking the event loop.
        - The `convert` function is a CPU-intensive function, so it is run in a separate process to avoid blocking the event loop and GIL.
    """
    if not video_capture.isOpened():
        return placeholder
# The `video_capture.read` call is a blocking function.
    # So we run it in a separate thread (default executor) to avoid blocking the event loop.
    _, frame = await run.io_bound(video_capture.read)
    if frame is None:
        return placeholder
# `convert` is a CPU-intensive function, so we run it in a separate process to avoid blocking the event loop and GIL.
    jpeg = await run.cpu_bound(convert, frame)
    return Response(content=jpeg, media_type='image/jpeg')

# For non-flickering image updates an interactive image is much better than `ui.image()`.
video_image = ui.interactive_image().classes('w-full h-full')
# A timer constantly updates the source of the image.
# Because data from same paths are cached by the browser,
# we must force an update by adding the current timestamp to the source.
ui.timer(interval=0.1, callback=lambda: video_image.set_source(f'/video/frame?{time.time()}'))


async def disconnect() -> None:
    """Disconnect all clients from the current running server.

    This function iterates over all connected clients and disconnects them from the server.
    It uses the `Client.instances` list to get the IDs of all connected clients.

    Example usage:
    ```
    await disconnect()
    ```

    Returns:
        None
    """
    for client_id in Client.instances:
        await core.sio.disconnect(client_id)


def handle_sigint(signum, frame) -> None:
    """
    Handle the SIGINT signal.

    This function is called when a SIGINT signal (e.g., Ctrl+C) is received. It performs the following actions:
    1. Calls the `disconnect` function asynchronously from the event loop using `ui.timer`.
    2. Delays the execution of the default SIGINT handler to allow the disconnect to complete.

    Parameters:
    - signum (int): The signal number.
    - frame (frame): The current stack frame.

    Returns:
    None
    """
    # `disconnect` is async, so it must be called from the event loop; we use `ui.timer` to do so.
    ui.timer(0.1, disconnect, once=True)
    # Delay the default handler to allow the disconnect to complete.
    ui.timer(1, lambda: signal.default_int_handler(signum, frame), once=True)


async def cleanup() -> None:
    """
    Cleans up resources used by the webcam application.

    This function disconnects any connected clients and releases the webcam hardware,
    allowing it to be used by other applications. It should be called when the webcam
    application is no longer needed.

    Returns:
        None
    """
    await disconnect()
    # Release the webcam hardware so it can be used by other applications again.
    video_capture.release()

app.on_shutdown(cleanup)
# We also need to disconnect clients when the app is stopped with Ctrl+C,
# because otherwise they will keep requesting images which lead to unfinished subprocesses blocking the shutdown.
signal.signal(signal.SIGINT, handle_sigint)

ui.run()
