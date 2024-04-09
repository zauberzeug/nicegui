import base64

from audio_recorder import AudioRecorder
from nicegui import ui


class AudioData:
    def __init__(self):
        self.audio_byte64 = None

    def set_audio_byte64(self, audio_data):
        self.audio_byte64 = audio_data.args["audioBlobBase64"]

    def get_audio_bytes(self):
        audio_data = self.audio_byte64.encode()
        content = base64.b64decode(audio_data)

        return content


@ui.page("/")
async def index():
    audio_data = AudioData()

    with ui.row().classes("w-full justify-center"):
        audio_recorder = AudioRecorder(on_audio_ready=audio_data.set_audio_byte64)

    with ui.row().classes("w-full justify-center"):
        ui.button(
            "Play",
            on_click=lambda: audio_recorder.play_recorded_audio()
            if audio_data.audio_byte64
            else ui.notify("No data to Play"),
        )
        ui.button(
            "Download",
            on_click=lambda: ui.download(audio_data.get_audio_bytes(), "audio.ogx")
            if audio_data.audio_byte64
            else ui.notify("No data to download"),
        )


ui.run()
