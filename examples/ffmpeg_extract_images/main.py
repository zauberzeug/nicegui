#!/usr/bin/env python3
import shutil
import subprocess
from pathlib import Path

from nicegui import events, run, ui

DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)


async def handle_upload(args: events.UploadEventArguments):
    if not args.file.content_type.startswith('video/'):
        ui.notify('Please upload a video file')
        return

    shutil.rmtree(DATA_DIR, ignore_errors=True)
    DATA_DIR.mkdir(exist_ok=True)

    video_path = DATA_DIR / args.file.name
    video_path.write_bytes(await args.file.read())

    with results.clear():
        ui.spinner('dots', size='xl')

    await run.io_bound(subprocess.call, ['ffmpeg', '-i', video_path, '-vf', 'fps=1', str(DATA_DIR / 'out_%04d.jpg')])

    with results.clear():
        for image_path in DATA_DIR.glob('*.jpg'):
            ui.image(image_path).classes('w-96 drop-shadow-md rounded')

    upload.run_method('reset')

with ui.column().classes('w-full items-center'):
    ui.label('Extract images from video').classes('text-3xl m-3')
    upload = ui.upload(label='Pick a video file', auto_upload=True, on_upload=handle_upload)
    results = ui.row().classes('w-full justify-center mt-6')

ui.run()
