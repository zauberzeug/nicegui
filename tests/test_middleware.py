import os

import httpx
import pytest
from fastapi.middleware.gzip import GZipMiddleware

from nicegui import app, ui
from nicegui.testing import Screen


@pytest.fixture
def _hide_is_pytest():
    os.environ['HIDE_IS_PYTEST'] = '1'
    yield
    os.environ.pop('HIDE_IS_PYTEST', None)


def test_gzip_middleware(_hide_is_pytest, screen: Screen):
    app.add_middleware(GZipMiddleware, minimum_size=9999999999999999)

    @ui.page('/')
    def main_page():
        ui.label('Hello, world!')

    screen.open('/')
    response = httpx.get(screen.url)
    assert 'gzip' not in response.headers.get('Content-Encoding', '')
