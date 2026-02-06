from nicegui import APIRouter, app, ui
from nicegui.testing import SharedScreen


def test_prefix(shared_screen: SharedScreen):
    router = APIRouter(prefix='/some-prefix')

    @router.page('/')
    def page():
        ui.label('Hello, world!')

    app.include_router(router)

    shared_screen.open('/some-prefix')
    shared_screen.should_contain('NiceGUI')
    shared_screen.should_contain('Hello, world!')


def test_passing_page_parameters(shared_screen: SharedScreen):
    router = APIRouter()

    @router.page('/', title='My Custom Title')
    def page():
        ui.label('Hello, world!')

    app.include_router(router)

    shared_screen.open('/')
    shared_screen.should_contain('My Custom Title')
