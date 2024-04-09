from typing import Callable, Optional

from nicegui.element import Element


class AudioRecorder(Element, component="audio_recorder.vue"):
    def __init__(self, *, on_audio_ready: Optional[Callable] = None) -> None:
        super().__init__()
        self.on("audio_ready", on_audio_ready)

    def start_recording(self) -> None:
        self.run_method("startRecording")

    def stop_recording(self) -> None:
        self.run_method("stopRecording")

    def play_recorded_audio(self) -> None:
        self.run_method("playRecordedAudio")
