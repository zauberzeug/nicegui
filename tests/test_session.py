from nicegui import globals, ui

from .screen import Screen


def test_session_data_is_stored_in_the_browser(screen: Screen):
    @ui.page('/')
    def page():
        globals.get_request().session['count'] = globals.get_request().session.get('count', 0) + 1
        ui.label(globals.get_request().session['count'])

    screen.open('/')
    screen.should_contain('1')
    screen.open('/')
    screen.should_contain('2')
    screen.open('/')
    screen.should_contain('3')
