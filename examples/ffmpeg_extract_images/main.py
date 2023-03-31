#!/usr/bin/env python3
import asyncio
import os
import pathlib
import shlex
import shutil
import subprocess

from nicegui import app, events, ui


def extract(source: str):
    subprocess.call(shlex.split(f'ffmpeg -i "{source}" -vf fps=1 out_%04d.jpg'))


async def handle_upload(args: events.UploadEventArguments):
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
