from pathlib import Path
from typing import Generator

import pytest
from fastapi.responses import PlainTextResponse

from nicegui import app, ui
from nicegui.testing import Screen, screen_plugin


@pytest.fixture
def test_route() -> Generator[str, None, None]:
    TEST_ROUTE = '/static/test.txt'
    yield TEST_ROUTE
    app.remove_route(TEST_ROUTE)


def test_download_text_file(screen: Screen, test_route: str):  # pylint: disable=redefined-outer-name
    @app.get(test_route)
    def test(number: str):
        return PlainTextResponse(f'test {number}')

    ui.button('Download 1', on_click=lambda: ui.download(test_route + '?number=1', 'test1.txt'))
    ui.button('Download 2', on_click=lambda: ui.download.from_url(test_route + '?number=2', 'test2.txt'))

    screen.open('/')
    screen.click('Download 1')
    screen.wait(0.5)
    assert (screen_plugin.DOWNLOAD_DIR / 'test1.txt').read_text(encoding='utf-8') == 'test 1'

    screen.click('Download 2')
    screen.wait(0.5)
    assert (screen_plugin.DOWNLOAD_DIR / 'test2.txt').read_text(encoding='utf-8') == 'test 2'


def test_downloading_local_file_as_src(screen: Screen):
    IMAGE_FILE1 = Path(__file__).parent.parent / 'examples' / 'slideshow' / 'slides' / 'slide1.jpg'
    IMAGE_FILE2 = Path(__file__).parent.parent / 'examples' / 'slideshow' / 'slides' / 'slide2.jpg'
    ui.button('Download 1', on_click=lambda: ui.download(IMAGE_FILE1))
    ui.button('Download 2', on_click=lambda: ui.download.file(IMAGE_FILE2))

    screen.open('/')
    route_count_before_download = len(app.routes)
    screen.click('Download 1')
    screen.wait(0.5)
    assert (screen_plugin.DOWNLOAD_DIR / 'slide1.jpg').exists()
    assert len(app.routes) == route_count_before_download

    screen.click('Download 2')
    screen.wait(0.5)
    assert (screen_plugin.DOWNLOAD_DIR / 'slide2.jpg').exists()
    assert len(app.routes) == route_count_before_download


def test_download_raw_data(screen: Screen):
    ui.button('Download 1', on_click=lambda: ui.download(b'test 1', 'test1.txt'))
    ui.button('Download 2', on_click=lambda: ui.download.content(b'test 2', 'test2.txt'))
    ui.button('Download 3', on_click=lambda: ui.download.content('test 3', 'test3.txt'))

    screen.open('/')
    screen.click('Download 1')
    screen.wait(0.5)
    assert (screen_plugin.DOWNLOAD_DIR / 'test1.txt').read_text(encoding='utf-8') == 'test 1'

    screen.click('Download 2')
    screen.wait(0.5)
    assert (screen_plugin.DOWNLOAD_DIR / 'test2.txt').read_text(encoding='utf-8') == 'test 2'

    screen.click('Download 3')
    screen.wait(0.5)
    assert (screen_plugin.DOWNLOAD_DIR / 'test3.txt').read_text(encoding='utf-8') == 'test 3'
