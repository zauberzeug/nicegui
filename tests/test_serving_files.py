import re
from pathlib import Path

import httpx
import pytest

from nicegui import __version__, app, ui
from nicegui.testing import SharedScreen

from .test_helpers import TEST_DIR

IMAGE_FILE = Path(TEST_DIR) / 'media' / 'test1.jpg'
VIDEO_FILE = Path(TEST_DIR) / 'media' / 'test.mp4'
VIDEO_FILE.parent.mkdir(exist_ok=True)
VIDEO_FILE.write_bytes(b'\x00' * 2000)  # dummy video file large enough to be streamed


@pytest.fixture
def secret_file():
    secret_path = Path(TEST_DIR) / '.env'
    secret_path.write_text('TOP SECRET DATA')
    yield secret_path
    secret_path.unlink(missing_ok=True)


def assert_video_file_streaming(path: str) -> None:
    with httpx.Client() as http_client:
        r = http_client.get(
            path if 'http' in path else f'http://localhost:{SharedScreen.PORT}{path}',
            headers={'Range': 'bytes=0-1000'},
        )
        assert r.status_code == 206
        assert r.headers['Accept-Ranges'] == 'bytes'
        assert r.headers['Content-Range'].startswith('bytes 0-1000/')
        assert r.headers['Content-Length'] == '1001'
        assert r.headers['Content-Type'] == 'video/mp4'


def test_media_files_can_be_streamed(shared_screen: SharedScreen):
    app.add_media_files('/media', Path(TEST_DIR) / 'media')

    @ui.page('/')
    def page():
        ui.label('Hello, world!')

    shared_screen.open('/')
    assert_video_file_streaming('/media/test.mp4')


def test_media_files_against_path_traversal(shared_screen: SharedScreen, secret_file):
    app.add_media_files('/media', Path(TEST_DIR) / 'media')

    @ui.page('/')
    def page():
        ui.label('Hello, world!')

    shared_screen.open('/')

    with httpx.Client() as http_client:
        r = http_client.get(f'http://localhost:{SharedScreen.PORT}/media/%2e%2e/.env')
        assert 'TOP SECRET DATA' not in r.text
        assert r.status_code == 404


def test_adding_single_media_file(shared_screen: SharedScreen):
    url_path = app.add_media_file(local_file=VIDEO_FILE)

    @ui.page('/')
    def page():
        ui.label('Hello, world!')

    shared_screen.open('/')
    assert_video_file_streaming(url_path)


@pytest.mark.parametrize('url_path', ['/static', '/static/'])
def test_get_from_static_files_dir(url_path: str, shared_screen: SharedScreen):
    app.add_static_files(url_path, Path(TEST_DIR).parent, max_cache_age=3456)

    @ui.page('/')
    def page():
        ui.label('Hello, world!')

    shared_screen.open('/')
    with httpx.Client() as http_client:
        r = http_client.get(f'http://localhost:{SharedScreen.PORT}/static/examples/slideshow/slides/slide1.jpg')
        assert r.status_code == 200
        assert 'max-age=3456' in r.headers['Cache-Control']


def test_404_for_non_existing_static_file(shared_screen: SharedScreen):
    app.add_static_files('/static', Path(TEST_DIR))

    @ui.page('/')
    def page():
        ui.label('Hello, world!')

    shared_screen.open('/')
    with httpx.Client() as http_client:
        r = http_client.get(f'http://localhost:{SharedScreen.PORT}/static/does_not_exist.jpg')
        shared_screen.assert_py_logger('WARNING', re.compile('.*does_not_exist.jpg not found'))
        assert r.status_code == 404
        assert 'static/_nicegui' not in r.text, 'should use root_path, see https://github.com/zauberzeug/nicegui/issues/2570'


def test_adding_single_static_file(shared_screen: SharedScreen):
    url_path = app.add_static_file(local_file=IMAGE_FILE, max_cache_age=3456)

    @ui.page('/')
    def page():
        ui.label('Hello, world!')

    shared_screen.open('/')
    with httpx.Client() as http_client:
        r = http_client.get(f'http://localhost:{SharedScreen.PORT}{url_path}')
        assert r.status_code == 200
        assert 'max-age=3456' in r.headers['Cache-Control']


def test_auto_serving_file_from_image_source(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.image(IMAGE_FILE)

    shared_screen.open('/')
    img = shared_screen.find_by_tag('img')
    assert '/_nicegui/auto/static/' in img.get_attribute('src')
    shared_screen.wait(0.5)
    assert shared_screen.selenium.execute_script('''
    return arguments[0].complete &&
        typeof arguments[0].naturalWidth != "undefined" &&
        arguments[0].naturalWidth > 0
    ''', img), 'image should load successfully'


def test_auto_serving_file_from_video_source(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.video(VIDEO_FILE)

    shared_screen.open('/')
    video = shared_screen.find_by_tag('video')
    assert '/_nicegui/auto/media/' in video.get_attribute('src')
    assert_video_file_streaming(video.get_attribute('src'))


def test_mimetypes_of_static_files(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.label('Hello, world!')

    shared_screen.open('/')

    response = httpx.get(f'http://localhost:{SharedScreen.PORT}/_nicegui/{__version__}/static/vue.esm-browser.js', timeout=5)
    assert response.status_code == 200
    assert response.headers['Content-Type'].startswith('text/javascript')

    response = httpx.get(f'http://localhost:{SharedScreen.PORT}/_nicegui/{__version__}/static/dompurify.mjs', timeout=5)
    assert response.status_code == 200
    assert response.headers['Content-Type'].startswith('text/javascript')

    response = httpx.get(f'http://localhost:{SharedScreen.PORT}/_nicegui/{__version__}/static/nicegui.css', timeout=5)
    assert response.status_code == 200
    assert response.headers['Content-Type'].startswith('text/css')


def test_cache_control_header_of_static_files(shared_screen: SharedScreen):
    app.add_static_files('/static', Path(TEST_DIR).parent)

    @ui.page('/')
    def page():
        ui.markdown()

    shared_screen.open('/')

    # resources are served with cache-control headers from `ui.run`
    response1 = httpx.get(f'http://localhost:{SharedScreen.PORT}/_nicegui/{__version__}/static/nicegui.css', timeout=5)
    assert 'immutable' in response1.headers.get('Cache-Control', '')

    # dynamic resources are _not_ served with cache-control headers from `ui.run`
    response2 = httpx.get(
        f'http://localhost:{SharedScreen.PORT}/_nicegui/{__version__}/dynamic_resources/codehilite.css', timeout=5)
    assert 'immutable' not in response2.headers.get('Cache-Control', '')

    # static resources are _not_ served with cache-control headers from `ui.run`
    response3 = httpx.get(f'http://localhost:{SharedScreen.PORT}/static/examples/slideshow/slides/slide1.jpg', timeout=5)
    assert 'immutable' not in response3.headers.get('Cache-Control', '')
