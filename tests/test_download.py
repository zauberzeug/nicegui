from typing import Generator

import pytest
from fastapi import HTTPException

from nicegui import app, ui

from .screen import Screen


@pytest.fixture
def test_route() -> Generator[str, None, None]:
    TEST_ROUTE = '/static/test.py'
    yield TEST_ROUTE
    app.remove_route(TEST_ROUTE)


def test_download(screen: Screen, test_route: str):
    success = False

    @app.get(test_route)
    def test():
        nonlocal success
        success = True
        raise HTTPException(404, 'Not found')

    ui.button('Download', on_click=lambda: ui.download(test_route))

    screen.open('/')
    screen.click('Download')
    screen.wait(0.5)
    assert success
    screen.assert_py_logger('WARNING', f'http://localhost:{Screen.PORT}{test_route} not found')
