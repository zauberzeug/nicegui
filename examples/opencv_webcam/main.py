#!/usr/bin/env python3
import asyncio
import base64
import concurrent.futures
import time
from typing import Optional

import cv2
import numpy as np
from fastapi import Response

from nicegui import app, ui

# we need two executors to schedule IO and CPU intensive tasks with loop.run_in_executor()
process_pool_executor = concurrent.futures.ProcessPoolExecutor()
thread_pool_executor = concurrent.futures.ThreadPoolExecutor()

# in case you don't have a webcam, this will provide a black placeholder image
black_1px = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAA1JREFUGFdjYGBg+A8AAQQBAHAgZQsAAAAASUVORK5CYII='
placeholder = Response(content=base64.b64decode(black_1px.encode('ascii')), media_type='image/png')

# OpenCV is used to access the webcam
video_capture = cv2.VideoCapture(0)


def convert(frame: np.ndarray) -> Optional[bytes]:
    _, imencode_image = cv2.imencode('.jpg', frame)
    return imencode_image.tobytes()


@app.get('/video/frame')
# thanks to FastAPI's "app.get" it is easy to create a web route which always provides the latest image from OpenCV
async def grab_video_frame() -> Response:
    loop = asyncio.get_running_loop()
    if not video_capture.isOpened():
        return placeholder
    # video_capture.read() is a blocking function, so we run it in a separate thread it to avoid blocking the event loop
    _, frame = await loop.run_in_executor(thread_pool_executor, video_capture.read)
    if frame is None:
        return placeholder
    # convert() is a cpu intensive function, so we run it in a separate process to avoid blocking the event loop and GIL
    jpeg = await loop.run_in_executor(process_pool_executor, convert, frame)
    if not jpeg:
        return placeholder
    return Response(content=jpeg, media_type='image/jpeg')

# For non-flickering image updates an interactive image is much better than ui.image().
video_image = ui.interactive_image().classes('w-full h-full')
# A timer constantly updates the source of the image.
# But because the path is always the same, we must force an update by adding the current timestamp to the source.
ui.timer(interval=0.01, callback=lambda: video_image.set_source(f'/video/frame?{time.time()}'))

# the process pool executor must be shutdown when the app is closed, otherwise the process will not exit
app.on_shutdown(lambda: process_pool_executor.shutdown(wait=True, cancel_futures=True))

ui.run()
