#!/usr/bin/env python3
import asyncio
import base64
import concurrent.futures
import signal
import time
from typing import Optional

import cv2
import numpy as np
import psutil
from fastapi import Response
from icecream import ic

from nicegui import app
from nicegui import globals as nicegui_globals
from nicegui import ui

# we need two executors to schedule IO and CPU intensive tasks with loop.run_in_executor()
process_pool_executor = concurrent.futures.ProcessPoolExecutor()
thread_pool_executor = concurrent.futures.ThreadPoolExecutor()

# in case you don't have a webcam, this will provide a black placeholder image
black_1px = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAA1JREFUGFdjYGBg+A8AAQQBAHAgZQsAAAAASUVORK5CYII='
placeholder = Response(content=base64.b64decode(black_1px.encode('ascii')), media_type='image/png')

# OpenCV is used to access the webcam
video_capture = cv2.VideoCapture(0)


def convert(frame: np.ndarray) -> Optional[bytes]:
    if not frame_updater.active:
        return None
    _, imencode_image = cv2.imencode('.jpg', frame)
    return imencode_image.tobytes()


@app.get('/video/frame')
# thanks to FastAPI's "app.get" it is easy to create a web route which always provides the latest image from OpenCV
async def grab_video_frame() -> Response:
    if not frame_updater.active:
        return placeholder
    loop = asyncio.get_running_loop()
    if not video_capture.isOpened():
        return placeholder
    # the video_capture.read call is a blocking function, so we run it in a separate thread it to avoid blocking the event loop
    _, frame = await loop.run_in_executor(thread_pool_executor, video_capture.read)
    if frame is None:
        return placeholder
    # "convert" is a cpu intensive function, so we run it in a separate process to avoid blocking the event loop and GIL
    jpeg = await loop.run_in_executor(process_pool_executor, convert, frame)
    if not jpeg:
        return placeholder
    return Response(content=jpeg, media_type='image/jpeg')

# For non-flickering image updates an interactive image is much better than ui.image().
video_image = ui.interactive_image().classes('w-full h-full')
# A timer constantly updates the source of the image.
# Because data from same paths are cached by the browser, we must force an update by adding the current timestamp to the source.
frame_updater = ui.timer(interval=0.1, callback=lambda: video_image.set_source(f'/video/frame?{time.time()}'))


def stop_updates(signum, frame):
    frame_updater.active = False
    ui.timer(1, lambda: signal.default_int_handler(signum, frame), once=True)


async def cleanup():
    for client in nicegui_globals.clients.keys():
        await app.sio.disconnect(client)
    video_capture.release()
    thread_pool_executor.shutdown()
    # the process pool executor must be shutdown when the app is closed, otherwise the process will not exit
    process_pool_executor.shutdown()
    await asyncio.sleep(1)

app.on_shutdown(cleanup)

signal.signal(signal.SIGINT, stop_updates)

ui.run()
