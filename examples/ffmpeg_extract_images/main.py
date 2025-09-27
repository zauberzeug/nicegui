#!/usr/bin/env python3
import shutil
import subprocess
from pathlib import Path

import aiofiles

from nicegui import app, events, run, ui


def extract(source: Path, output_dir: Path):
    subprocess.call(['ffmpeg', '-i', str(source), '-vf', 'fps=1', str(output_dir / 'out_%04d.jpg')])


async def handle_upload(args: events.UploadEventArguments):
    if 'video' in args.type:
        data_dir = Path('data')
        shutil.rmtree(data_dir, ignore_errors=True)
        data_dir.mkdir(exist_ok=True)

        file_path = data_dir / args.name
        async with aiofiles.open(file_path, 'wb') as f:
            data = await args.file.read()
            await f.write(data)

        results.clear()
        with results:
            ui.spinner('dots', size='xl')

        run.io_bound(extract(file_path, data_dir))

        results.clear()
        with results:
            for path in data_dir.glob('*.jpg'):
                ui.image(f'/data/{path.name}').classes('w-96 drop-shadow-md rounded')
    else:
        ui.notify('Please upload a video file')
    upload.run_method('reset')

Path('data').mkdir(exist_ok=True)
app.add_static_files('/data', 'data')

with ui.column().classes('w-full items-center'):
    ui.label('Extract images from video').classes('text-3xl m-3')
    upload = ui.upload(label='pick a video file', auto_upload=True, on_upload=handle_upload)
    results = ui.row().classes('w-full justify-center mt-6')

ui.run()
