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
    screen.wait_for(lambda: len(results) == 1)
    assert results[0].file.content_type.startswith('audio/')
    assert len(await results[0].file.read()) > 1000


def test_unsupported_mime_type_reports_error(screen: Screen):
    @ui.page('/')
    def page():
        recorder = ui.audio_recorder(mime_type='audio/x-unsupported',
                                     on_error=lambda e: ui.label(f'Error: {e.args["name"]}'))
        ui.button('Start', on_click=recorder.start)

    screen.open('/')
    screen.click('Start')
    screen.should_contain('Error: NotSupportedError')


def test_stop_before_microphone_is_ready_reports_error(screen: Screen):
    @ui.page('/')
    def page():
        ui.add_head_html('''<script>
            const getUserMedia = navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices);
            navigator.mediaDevices.getUserMedia = (c) => new Promise((r) => setTimeout(r, 1000)).then(() => getUserMedia(c));
        </script>''')
        recorder = ui.audio_recorder(on_error=lambda e: ui.label(f'Error: {e.args["name"]}'))
        ui.button('Start', on_click=recorder.start)
        ui.button('Stop', on_click=recorder.stop)

    screen.open('/')
    screen.click('Start')
    screen.click('Stop')
    screen.should_contain('Error: AbortError')
