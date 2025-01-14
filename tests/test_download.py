from pathlib import Path
from typing import Generator

import pytest
from fastapi.responses import PlainTextResponse

from nicegui import app, ui
from nicegui.app import app as app_module
from nicegui.testing import Screen, screen_plugin


@pytest.fixture
def test_route() -> Generator[str, None, None]:
    TEST_ROUTE = '/static/test.txt'
    yield TEST_ROUTE
    app.remove_route(TEST_ROUTE)


def test_download_text_file(screen: Screen, test_route: str):  # pylint: disable=redefined-outer-name
    @app.get(test_route)
    def test():
        return PlainTextResponse('test')

    ui.button('Download', on_click=lambda: ui.download(test_route))

    screen.open('/')
    screen.click('Download')
    screen.wait(0.5)
    assert (screen_plugin.DOWNLOAD_DIR / 'test.txt').read_text() == 'test'


def test_downloading_local_file_as_src(screen: Screen):
    IMAGE_FILE = Path(__file__).parent.parent / 'examples' / 'slideshow' / 'slides' / 'slide1.jpg'
    ui.button('download', on_click=lambda: ui.download(IMAGE_FILE))
    app_module.SINGLE_USE_ROUTE_TIMEOUT = 0.1

    screen.open('/')
    route_count_before_download = len(app.routes)
    screen.click('download')
    screen.wait(0.5)
    assert (screen_plugin.DOWNLOAD_DIR / 'slide1.jpg').exists()
    assert len(app.routes) == route_count_before_download


def test_download_raw_data(screen: Screen):
    ui.button('download', on_click=lambda: ui.download(b'test', 'test.txt'))

    screen.open('/')
    screen.click('download')
    screen.wait(0.5)
    assert (screen_plugin.DOWNLOAD_DIR / 'test.txt').read_text() == 'test'
