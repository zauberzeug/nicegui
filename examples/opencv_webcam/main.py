#!/usr/bin/env python3
import base64
import time

import cv2
from fastapi import Response

from nicegui import app, ui

# in case you don't have a webcam, this will provide a black placeholder image
black_1px = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAA1JREFUGFdjYGBg+A8AAQQBAHAgZQsAAAAASUVORK5CYII='
placeholder = Response(content=base64.b64decode(black_1px.encode('ascii')), media_type='image/png')

# openCV is used to accesss the webcam
video_capture = cv2.VideoCapture(0)


@app.get('/video/frame')
async def grab_video_frame() -> Response:
    # thanks to FastAPI it's easy to create a web route which always provides the latest image from openCV
    if not video_capture.isOpened():
        return placeholder
    ret, frame = video_capture.read()
    if not ret:
        return placeholder
    _, imencode_image = cv2.imencode('.jpg', frame)
    jpeg = imencode_image.tobytes()
    return Response(content=jpeg, media_type='image/jpeg')

# For non-flickering image updates an interactive image is much better than ui.image()
video_image = ui.interactive_image().classes('w-full h-full')
# A timer constantly updates the source of the image.
# But because the path is always the same, we must force an update by adding the current timestamp to the source.
ui.timer(interval=0.1, callback=lambda: video_image.set_source(f'/video/frame?{time.time()}'))

ui.run()
