from nicegui import events, ui
from nicegui.testing import Screen


async def test_recording_arrives_on_server(screen: Screen):
    results: list[events.UploadEventArguments] = []

    @ui.page('/')
    def page():
        recorder = ui.audio_recorder(on_audio_ready=results.append)
        ui.button('Start', on_click=recorder.start)
        ui.button('Stop', on_click=recorder.stop)

    screen.open('/')
    screen.click('Start')
    screen.wait(1.0)
    screen.click('Stop')
    screen.wait(0.5)
    assert len(results) == 1
    assert results[0].file.content_type.startswith('audio/')
    assert len(await results[0].file.read()) > 1000
