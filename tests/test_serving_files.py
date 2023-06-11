
import os
from pathlib import Path

import httpx
import pytest

from nicegui import app, ui

from .screen import PORT, Screen
from .test_helpers import TEST_DIR


@pytest.fixture(autouse=True)
def provide_media_files():
    mp4 = Path(TEST_DIR / 'media' / 'test.mp4')
    if not mp4.exists():
        mp4.parent.mkdir(exist_ok=True)
        url = 'https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4'
        with httpx.stream('GET', url) as response:
            with open(mp4, 'wb') as file:
                for chunk in response.iter_raw():
                    file.write(chunk)


def assert_video_file_streaming(path: str) -> None:
    with httpx.Client() as http_client:
        r = http_client.get(f'http://localhost:{PORT}{path}', headers={'Range': 'bytes=0-1000'})
        assert r.status_code == 206
        assert r.headers['Accept-Ranges'] == 'bytes'
        assert r.headers['Content-Range'].startswith('bytes 0-1000/')
        assert r.headers['Content-Length'] == '1001'
        assert r.headers['Content-Type'] == 'video/mp4'


def test_media_files_can_be_streamed(screen: Screen):
    app.add_media_files('/media', Path(TEST_DIR) / 'media')
    screen.open('/')
    assert_video_file_streaming('/media/test.mp4')


def test_adding_single_media_file(screen: Screen):
    url_path = app.add_media_file(Path(TEST_DIR) / 'media' / 'test.mp4')

    screen.open('/')
    assert_video_file_streaming(url_path)
