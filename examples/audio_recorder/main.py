#!/usr/bin/env python3
import base64

from nicegui import events, ui

last_recording: events.UploadEventArguments | None = None


async def handle_audio(e: events.UploadEventArguments) -> None:
    global last_recording  # pylint: disable=global-statement # noqa: PLW0603
    last_recording = e
    data = await e.file.read()
    player.set_source(f'data:{e.file.content_type};base64,{base64.b64encode(data).decode()}')
    player.set_visibility(True)
    download.enable()
    ui.notify(f'Recorded {len(data)} bytes')


async def download_recording() -> None:
    if last_recording:
        ui.download(await last_recording.file.read(), last_recording.file.name)

recorder = ui.audio_recorder(on_audio_ready=handle_audio,
                             on_error=lambda e: ui.notify(e.args['message'], type='negative'))

with ui.column().classes('w-full items-center'):
    ui.button('Hold to Record', color='red').classes('rounded-full w-28 h-28') \
        .on('mousedown', recorder.start).on('mouseup', recorder.stop) \
        .on('touchstart', recorder.start).on('touchend', recorder.stop)
    player = ui.audio('')
    player.set_visibility(False)
    download = ui.button('Download', icon='download', on_click=download_recording)
    download.disable()

ui.run()
