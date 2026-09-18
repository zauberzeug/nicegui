from nicegui import APIRouter, app, ui
from nicegui.testing import Screen


def test_prefix(screen: Screen):
    router = APIRouter(prefix='/some-prefix')

    @router.page('/')
    def page():
        ui.label('Hello, world!')

    app.include_router(router)

    screen.open('/some-prefix')
    screen.should_contain('NiceGUI')
    screen.should_contain('Hello, world!')


def test_passing_page_parameters(screen: Screen):
    router = APIRouter()

    @router.page('/', title='My Custom Title')
    def page():
        ui.label('Hello, world!')

    app.include_router(router)

    screen.open('/')
    screen.should_contain('My Custom Title')


def test_relative_navigation_from_router_root_page(screen: Screen):
    router = APIRouter(prefix='/some-prefix')

    @router.page('/')
    def root():
        ui.button('Go', on_click=lambda: ui.navigate.to('4711'))

    @router.page('/{key:int}')
    def detail(key: int):
        ui.label(f'Detail {key}')

    app.include_router(router)

    screen.open('/some-prefix')
    screen.click('Go')
    screen.should_contain('Detail 4711')
    assert screen.current_path == '/some-prefix/4711'
