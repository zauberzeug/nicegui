
from pathlib import Path

import httpx
import pytest
import requests

from nicegui import __version__, app, ui
from nicegui.testing import Screen

from .test_helpers import TEST_DIR

IMAGE_FILE = Path(TEST_DIR).parent / 'examples' / 'slideshow' / 'slides' / 'slide1.jpg'
VIDEO_FILE = Path(TEST_DIR) / 'media' / 'test.mp4'


@pytest.fixture(autouse=True)
def provide_media_files():
    if not VIDEO_FILE.exists():
        VIDEO_FILE.parent.mkdir(exist_ok=True)
        url = 'https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4'
        with httpx.stream('GET', url) as response:
            with open(VIDEO_FILE, 'wb') as file:
                for chunk in response.iter_raw():
                    file.write(chunk)


def assert_video_file_streaming(path: str) -> None:
    with httpx.Client() as http_client:
        r = http_client.get(
            path if 'http' in path else f'http://localhost:{Screen.PORT}{path}',
            headers={'Range': 'bytes=0-1000'},
            timeout=1,
        )
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
    url_path = app.add_media_file(local_file=VIDEO_FILE)

    screen.open('/')
    assert_video_file_streaming(url_path)


def test_adding_single_static_file(screen: Screen):
    url_path = app.add_static_file(local_file=IMAGE_FILE)

    screen.open('/')
    with httpx.Client() as http_client:
        r = http_client.get(f'http://localhost:{Screen.PORT}{url_path}')
        assert r.status_code == 200
        assert 'max-age=' in r.headers['Cache-Control']


def test_auto_serving_file_from_image_source(screen: Screen):
    ui.image(IMAGE_FILE)

    screen.open('/')
    img = screen.find_by_tag('img')
    assert '/_nicegui/auto/static/' in img.get_attribute('src')
    assert screen.selenium.execute_script("""
    return arguments[0].complete && 
        typeof arguments[0].naturalWidth != "undefined" && 
        arguments[0].naturalWidth > 0
    """, img), 'image should load successfully'


def test_auto_serving_file_from_video_source(screen: Screen):
    ui.video(VIDEO_FILE)

    screen.open('/')
    video = screen.find_by_tag('video')
    src = video.get_attribute('src')
    assert src is not None
    ic()
    assert '/_nicegui/auto/media/' in src
    ic()
    assert_video_file_streaming(src)
    ic()


def test_mimetypes_of_static_files(screen: Screen):
    screen.open('/')

    response = requests.get(f'http://localhost:{Screen.PORT}/_nicegui/{__version__}/static/vue.global.js', timeout=5)
    assert response.status_code == 200
    assert response.headers['Content-Type'].startswith('text/javascript')

    response = requests.get(f'http://localhost:{Screen.PORT}/_nicegui/{__version__}/static/nicegui.css', timeout=5)
    assert response.status_code == 200
    assert response.headers['Content-Type'].startswith('text/css')
