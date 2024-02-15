#!/usr/bin/env python3
import asyncio
import os
import pathlib
import shlex
import shutil
import subprocess

from nicegui import app, events, ui


def extract(source: str):
    """
    Extract frames from a video using FFmpeg.

    This function takes a video file as input and extracts frames from it using FFmpeg.
    The frames are saved as JPEG images with filenames in the format 'out_0001.jpg', 'out_0002.jpg', etc.

    Parameters:
    source (str): The path to the input video file.

    Returns:
    None

    Raises:
    FileNotFoundError: If the input video file does not exist.
    """

    subprocess.call(shlex.split(f'ffmpeg -i "{source}" -vf fps=1 out_%04d.jpg'))


async def handle_upload(args: events.UploadEventArguments):
    """
    Handle the upload of a video file and extract images from it using ffmpeg.

    Args:
        args (events.UploadEventArguments): The arguments passed to the event handler.

    Returns:
        None

    Raises:
        None

    Usage:
        This function is intended to be used as an event handler for file upload events.
        It expects the 'args' parameter to be an instance of the UploadEventArguments class.

    Behavior:
        - If the uploaded file is a video file, it extracts images from it using ffmpeg.
        - The extracted images are saved in the 'data' directory.
        - The spinner UI element is displayed while the extraction is in progress.
        - The extracted images are displayed in the UI as thumbnails.
        - If the uploaded file is not a video file, a notification is displayed.

    Note:
        - The 'data' directory will be cleared before extracting images from the video file.
        - The extracted images will be saved in the 'data' directory.
        - The UI elements used in this function are assumed to be defined elsewhere.

    Example:
        # Define the event handler
        async def handle_upload(args: events.UploadEventArguments):
            # Code for handling the upload

        # Register the event handler
        upload.on_event('upload', handle_upload)
    """
    if 'video' in args.type:
        shutil.rmtree('data', ignore_errors=True)
        os.makedirs('data', exist_ok=True)
        os.chdir('data')
        with open(args.name, 'wb') as f:
            f.write(args.content.read())
            results.clear()
            with results:
                ui.spinner('dots', size='xl')
            await asyncio.to_thread(extract, args.name)
            results.clear()
            with results:
                for path in pathlib.Path('.').glob('*.jpg'):
                    ui.image(f'/data/{path.name}').classes('w-96 drop-shadow-md rounded')
        os.chdir('..')
    else:
        ui.notify('Please upload a video file')
    upload.run_method('reset')

os.makedirs('data', exist_ok=True)
app.add_static_files('/data', 'data')

with ui.column().classes('w-full items-center'):
    ui.label('Extract images from video').classes('text-3xl m-3')
    upload = ui.upload(label='pick a video file', auto_upload=True, on_upload=handle_upload)
    results = ui.row().classes('w-full justify-center mt-6')

ui.run()
