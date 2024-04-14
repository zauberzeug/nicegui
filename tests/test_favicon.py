from pathlib import Path
from typing import Union

import requests
from bs4 import BeautifulSoup

from nicegui import favicon, ui
from nicegui.testing import Screen

DEFAULT_FAVICON_PATH = Path(__file__).parent.parent / 'nicegui' / 'static' / 'favicon.ico'
LOGO_FAVICON_PATH = Path(__file__).parent.parent / 'website' / 'static' / 'logo_square.png'


def assert_favicon_url_starts_with(screen: Screen, content: str):
    soup = BeautifulSoup(screen.selenium.page_source, 'html.parser')
    icon_link = soup.find('link', rel='icon')
    assert icon_link['href'].startswith(content)


def assert_favicon(content: Union[Path, str, bytes], url_path: str = '/favicon.ico'):
    response = requests.get(f'http://localhost:{Screen.PORT}{url_path}', timeout=5)
    assert response.status_code == 200
    if isinstance(content, Path):
        assert content.read_bytes() == response.content
    elif isinstance(content, str):
        assert content == response.text
    elif isinstance(content, bytes):
        assert content == response.content
    else:
        raise TypeError(f'Unexpected type: {type(content)}')


def test_default(screen: Screen):
    ui.label('Hello, world')

    screen.open('/')
    assert_favicon(DEFAULT_FAVICON_PATH)


def test_emoji(screen: Screen):
    ui.label('Hello, world')

    screen.ui_run_kwargs['favicon'] = '👋'
    screen.open('/')
    assert_favicon_url_starts_with(screen, 'data:image/svg+xml')
    assert_favicon(favicon._char_to_svg('👋'))


def test_data_url(screen: Screen):
    ui.label('Hello, world')

    icon = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='
    screen.ui_run_kwargs['favicon'] = icon
    screen.open('/')
    assert_favicon_url_starts_with(screen, 'data:image/png;base64')
    _, bytes_ = favicon._data_url_to_bytes(icon)
    assert_favicon(bytes_)


def test_custom_file(screen: Screen):
    ui.label('Hello, world')

    screen.ui_run_kwargs['favicon'] = LOGO_FAVICON_PATH
    screen.open('/')
    assert_favicon_url_starts_with(screen, '/favicon.ico')
    assert_favicon(screen.ui_run_kwargs['favicon'])


def test_page_specific_icon(screen: Screen):
    @ui.page('/subpage', favicon=LOGO_FAVICON_PATH)
    def sub():
        ui.label('Subpage')

    ui.label('Main')

    screen.open('/subpage')
    assert_favicon(LOGO_FAVICON_PATH, url_path='/subpage/favicon.ico')
    screen.open('/')


def test_page_specific_emoji(screen: Screen):
    @ui.page('/subpage', favicon='👋')
    def sub():
        ui.label('Subpage')

    ui.label('Main')

    screen.open('/subpage')
    assert_favicon_url_starts_with(screen, 'data:image/svg+xml')
    screen.open('/')
    assert_favicon(DEFAULT_FAVICON_PATH)
