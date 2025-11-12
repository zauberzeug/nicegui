import math
import wave
from array import array

import pytest

from nicegui import app, ui
from nicegui.testing import Screen

SONG1 = '/audio1.wav'
SONG2 = '/audio2.wav'


@pytest.fixture
def provide_audio_file(tmp_path):
    def create_sine_wave(filename, freq, duration=1.0, samplerate=44100):
        n_samples = int(samplerate * duration)
        amplitude = 32767  # max for int16
        samples = array('h')  # signed 16-bit

        for i in range(n_samples):
            t = i / samplerate
            value = int(amplitude * math.sin(2 * math.pi * freq * t))
            samples.append(value)

        with open(filename, 'wb') as f:
            with wave.Wave_write(f) as wav_file:
                wav_file.setnchannels(1)  # mono
                wav_file.setsampwidth(2)  # bytes per sample
                wav_file.setframerate(samplerate)
                wav_file.writeframes(samples.tobytes())

    file1 = tmp_path / 'test1.wav'
    file2 = tmp_path / 'test2.wav'
    create_sine_wave(file1, freq=440)  # A4
    create_sine_wave(file2, freq=554)  # C#5

    app.add_static_file(local_file=file1, url_path=SONG1)
    app.add_static_file(local_file=file2, url_path=SONG2)


def test_replace_audio(screen: Screen, provide_audio_file):
    @ui.page('/')
    def page():
        with ui.row() as container:
            ui.audio(SONG1)

        def replace():
            container.clear()
            with container:
                ui.audio(SONG2)
        ui.button('Replace', on_click=replace)

    screen.open('/')
    assert screen.find_by_tag('audio').get_attribute('src').endswith(SONG1)

    screen.click('Replace')
    screen.wait(0.5)
    assert screen.find_by_tag('audio').get_attribute('src').endswith(SONG2)


def test_change_source(screen: Screen, provide_audio_file):
    @ui.page('/')
    def page():
        audio = ui.audio(SONG1)
        ui.button('Change source', on_click=lambda: audio.set_source(SONG2))

    screen.open('/')
    assert screen.find_by_tag('audio').get_attribute('src').endswith(SONG1)

    screen.click('Change source')
    screen.wait(0.5)
    assert screen.find_by_tag('audio').get_attribute('src').endswith(SONG2)
