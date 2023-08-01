from fastapi import HTTPException

from nicegui import app, ui

from .screen import Screen


def test_download(screen: Screen):
    success = False

    @app.get('/static/test.py')
    def test():
        nonlocal success
        success = True
        raise HTTPException(404, 'Not found')

    ui.button('Download', on_click=lambda: ui.download('static/test.py'))

    screen.open('/')
    screen.click('Download')
    screen.wait(0.5)
    assert success
    screen.assert_py_logger('WARNING', f'http://localhost:{Screen.PORT}/static/test.py not found')
