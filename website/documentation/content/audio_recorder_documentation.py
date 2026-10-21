from nicegui import events, ui

from . import doc


@doc.demo(ui.audio_recorder)
def main_demo() -> None:
    async def handle_audio(e: events.UploadEventArguments) -> None:
        data = await e.file.read()
        ui.notify(f'Recorded {len(data)} bytes of {e.file.content_type}')

    recorder = ui.audio_recorder(on_audio_ready=handle_audio,
                                 on_error=lambda e: ui.notify(e.args['message'], type='negative'))
    ui.button('Start', icon='mic', on_click=recorder.start)
    ui.button('Stop', icon='stop', on_click=recorder.stop)


doc.reference(ui.audio_recorder)
