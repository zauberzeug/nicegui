from nicegui import app
from nicegui.testing import Screen


def test_404page_for_static_files(screen: Screen):
    app.add_static_files('/static', '.')

    screen.open('/static')
    screen.should_contain('This page doesn\'t exist.')
    screen.assert_py_logger('WARNING',f'http://localhost:{screen.PORT}/static/ not found')

    screen.open('/static/_____')
    screen.should_contain('This page doesn\'t exist.')
    screen.assert_py_logger('WARNING',f'http://localhost:{screen.PORT}/static/_____ not found')

    app.remove_route('/static')