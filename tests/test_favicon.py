from pathlib import Path

import requests
from bs4 import BeautifulSoup

from nicegui import ui

from .screen import PORT, Screen


def assert_favicon_url_starts_with(screen: Screen, content: str):
    soup = BeautifulSoup(screen.selenium.page_source, 'html.parser')
    icon_link = soup.find("link", rel="icon")
    assert icon_link['href'].startswith(content)


def test_default(screen: Screen):
    ui.label('Hello, world')

    screen.open('/')
    response = requests.get(f'http://localhost:{PORT}/favicon.ico')
    assert response.status_code == 200


def test_emoji(screen: Screen):
    ui.label('Hello, world')

    screen.ui_run_kwargs['favicon'] = '👋'
    screen.open('/')
    response = requests.get(f'http://localhost:{PORT}/favicon.ico')
    assert response.status_code == 200, 'default favicon should still be available for plain FastAPI requests running in the browser'
    assert (Path(__file__).parent.parent / 'nicegui' / 'static' / 'favicon.ico').read_bytes() == response.content
    assert_favicon_url_starts_with(screen, 'data:image/svg+xml')


def test_custom_file(screen: Screen):
    ui.label('Hello, world')

    screen.ui_run_kwargs['favicon'] = Path(__file__).parent.parent / 'website' / 'static' / 'logo_square.png'
    screen.open('/')
    assert_favicon_url_starts_with(screen, '/favicon.ico')
    response = requests.get(f'http://localhost:{PORT}/favicon.ico')
    assert response.status_code == 200
    assert screen.ui_run_kwargs['favicon'].read_bytes() == response.content
