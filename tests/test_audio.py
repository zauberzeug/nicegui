from nicegui import app, ui
from nicegui.testing import Screen


def _serve_empty_file(path: str):
    @app.get(path)
    def get_empty_file():
        return b''


def test_replace_audio(screen: Screen):
    _serve_empty_file(SONG1 := '/audio1.wav')
    _serve_empty_file(SONG2 := '/audio2.wav')

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


def test_change_source(screen: Screen):
    _serve_empty_file(SONG1 := '/audio1.wav')
    _serve_empty_file(SONG2 := '/audio2.wav')

    @ui.page('/')
    def page():
        audio = ui.audio(SONG1)
        ui.button('Change source', on_click=lambda: audio.set_source(SONG2))

    screen.open('/')
    assert screen.find_by_tag('audio').get_attribute('src').endswith(SONG1)

    screen.click('Change source')
    screen.wait(0.5)
    assert screen.find_by_tag('audio').get_attribute('src').endswith(SONG2)
