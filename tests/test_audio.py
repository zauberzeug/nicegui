from nicegui import app, ui
from nicegui.testing import SharedScreen


def _serve_empty_file(path: str):
    @app.get(path)
    def get_empty_file():
        return b''


def test_replace_audio(shared_screen: SharedScreen):
    _serve_empty_file(SONG1 := '/audio1.wav')
    _serve_empty_file(SONG2 := '/audio2.wav')

    @ui.page('/')
    def page():
        with ui.row() as container:
            ui.audio(SONG1)

        def replace():
            with container.clear():
                ui.audio(SONG2)
        ui.button('Replace', on_click=replace)

    shared_screen.open('/')
    assert shared_screen.find_by_tag('audio').get_attribute('src').endswith(SONG1)

    shared_screen.click('Replace')
    shared_screen.wait(0.5)
    assert shared_screen.find_by_tag('audio').get_attribute('src').endswith(SONG2)


def test_change_source(shared_screen: SharedScreen):
    _serve_empty_file(SONG1 := '/audio1.wav')
    _serve_empty_file(SONG2 := '/audio2.wav')

    @ui.page('/')
    def page():
        audio = ui.audio(SONG1)
        ui.button('Change source', on_click=lambda: audio.set_source(SONG2))

    shared_screen.open('/')
    assert shared_screen.find_by_tag('audio').get_attribute('src').endswith(SONG1)

    shared_screen.click('Change source')
    shared_screen.wait(0.5)
    assert shared_screen.find_by_tag('audio').get_attribute('src').endswith(SONG2)
