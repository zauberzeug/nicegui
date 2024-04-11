import base64
from typing import Callable, Optional

from nicegui import events, ui


class AudioRecorder(ui.element, component='audio_recorder.vue'):

    def __init__(self, *, on_audio_ready: Optional[Callable] = None) -> None:
        super().__init__()
        self.recording = b''

        def handle_audio(e: events.GenericEventArguments) -> None:
            self.recording = base64.b64decode(e.args['audioBlobBase64'].encode())
            if on_audio_ready:
                on_audio_ready(self.recording)
        self.on('audio_ready', handle_audio)

    def start_recording(self) -> None:
        self.run_method('startRecording')

    def stop_recording(self) -> None:
        self.run_method('stopRecording')

    def play_recorded_audio(self) -> None:
        self.run_method('playRecordedAudio')
