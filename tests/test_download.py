from pathlib import Path

from fastapi.responses import PlainTextResponse

from nicegui import app, ui

from .conftest import DOWNLOAD_DIR
from .screen import Screen

IMAGE_FILE = Path(__file__).parent.parent / 'examples' / 'slideshow' / 'slides' / 'slide1.jpg'


def test_download_text_file(screen: Screen):
    @app.get('/static/test.txt')
    def test():
        return PlainTextResponse('test')

    ui.button('Download', on_click=lambda: ui.download('static/test.txt'))

    screen.open('/')
    screen.click('Download')
    screen.wait(0.5)
    assert (DOWNLOAD_DIR / 'test.txt').read_text() == 'test'


def test_downloading_local_file_as_src(screen: Screen):
    ui.button('download', on_click=lambda: ui.download(IMAGE_FILE))

    screen.open('/')
    screen.click('download')
    screen.wait(0.5)
    assert (DOWNLOAD_DIR / 'slide1.jpg').exists()
