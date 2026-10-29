from nicegui import APIRouter, app, ui
from nicegui.client import Client
from nicegui.page import page
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


def test_page_route_includes_include_prefix():
    router = APIRouter()

    @router.page('/sub')
    def sub():
        ui.label('Sub')

    app.include_router(router, prefix='/v2')

    assert Client.page_routes[sub] == '/v2/sub'
    assert page.instances[sub].path == '/v2/sub'


def test_page_route_includes_nested_router_prefixes():
    inner = APIRouter(prefix='/inner')
    outer = APIRouter(prefix='/outer')

    @inner.page('/sub')
    def sub():
        ui.label('Sub')

    outer.include_router(inner)
    app.include_router(outer)

    assert Client.page_routes[sub] == '/outer/inner/sub'


def test_link_to_page_of_included_router(screen: Screen):
    router = APIRouter()

    @router.page('/sub')
    def sub():
        ui.label('Sub')

    app.include_router(router, prefix='/v2')

    @ui.page('/')
    def index():
        ui.link('Sub', sub)

    screen.open('/')
    screen.click('Sub')
    screen.should_contain('Sub')
    assert screen.current_path == '/v2/sub'


def test_favicon_route_includes_include_prefix(tmp_path):
    icon = tmp_path / 'icon.svg'
    icon.write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>', encoding='utf-8')

    router = APIRouter()

    @router.page('/sub', favicon=icon)
    def sub():
        ui.label('Sub')

    app.include_router(router, prefix='/v2')

    assert '/v2/sub/favicon.ico' in {getattr(route, 'path', None) for route in app.routes}
