from pathlib import Path

import requests
from bs4 import BeautifulSoup

from nicegui import ui

from .screen import PORT, Screen

DEFAULT_FAVICON_PATH = Path(__file__).parent.parent / 'nicegui' / 'static' / 'favicon.ico'
LOGO_FAVICON_PATH = Path(__file__).parent.parent / 'website' / 'static' / 'logo_square.png'


def assert_favicon_url_starts_with(screen: Screen, content: str):
    soup = BeautifulSoup(screen.selenium.page_source, 'html.parser')
    icon_link = soup.find("link", rel="icon")
    assert icon_link['href'].startswith(content)


def assert_favicon(file: Path, url_path: str = '/favicon.ico'):
    response = requests.get(f'http://localhost:{PORT}{url_path}')
    assert response.status_code == 200
    assert file.read_bytes() == response.content


def test_default(screen: Screen):
    ui.label('Hello, world')

    screen.open('/')
    assert_favicon(DEFAULT_FAVICON_PATH)


def test_emoji(screen: Screen):
    ui.label('Hello, world')

    screen.ui_run_kwargs['favicon'] = '👋'
    screen.open('/')
    assert_favicon_url_starts_with(screen, 'data:image/svg+xml')
    # the default favicon is still available (for example when accessing a plain FastAPI route with the browser)
    assert_favicon(DEFAULT_FAVICON_PATH)


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
