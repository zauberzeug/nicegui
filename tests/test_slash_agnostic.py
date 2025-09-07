import httpx
from fastapi import FastAPI

from nicegui import APIRouter, app, core, ui
from nicegui.middlewares import SlashAgnosticMiddleware
from nicegui.testing import Screen
from nicegui.testing.general_fixtures import prepare_simulation


def test_basic_rewriting_for_pages_and_get_requests(screen: Screen):
    @ui.page('/')
    def index():
        ui.label('index')

    @ui.page('/no-slash')
    def page_no_slash():
        ui.label('page without trailing slash')

    @ui.page('/with-slash/')
    def page_with_slash():
        ui.label('page with trailing slash')

    @app.get('/api-with-slash/')
    def api_with_slash():
        return {'ok': True, 'kind': 'with-slash'}

    screen.open('/no-slash/')
    screen.should_contain('page without trailing slash')
    assert screen.current_path == '/no-slash/'  # no redirect

    screen.open('/with-slash')
    screen.should_contain('page with trailing slash')
    assert screen.current_path == '/with-slash'  # no redirect

    # verify GET rewriting works without redirects
    r = httpx.get(f'http://localhost:{Screen.PORT}/api-with-slash', follow_redirects=False)
    assert r.status_code == 200
    assert r.json() == {'ok': True, 'kind': 'with-slash'}


def test_api_router_usage(screen: Screen):
    router = APIRouter(prefix='/router')

    @router.page('/page/')
    def router_page():
        ui.label('router page')

    @router.get('/data')
    def router_data():
        return {'data': 42}

    app.include_router(router)

    screen.open('/router/page')
    screen.should_contain('router page')
    assert screen.current_path == '/router/page'  # no redirect

    r = httpx.get(f'http://localhost:{Screen.PORT}/router/data/', follow_redirects=False)
    assert r.status_code == 200
    assert r.json() == {'data': 42}


async def test_root_path_is_respected(nicegui_reset_globals):
    prepare_simulation()

    @ui.page('/')
    def index():
        ui.label('root')

    @ui.page('/rp-slash/')
    def rp_page():
        ui.label('root_path page')

    @app.get('/rp-api')
    def rp_api():
        return {'ok': 'api'}

    # NOTE: ensure slash-agnostic behavior without starting uvicorn
    core.app.add_middleware(SlashAgnosticMiddleware)

    # NOTE simulate reverse proxy mounting by setting root_path in ASGI scope (async transport)
    transport = httpx.ASGITransport(core.app, root_path='/prefix')
    async with httpx.AsyncClient(transport=transport, base_url='http://test') as client:
        r1 = await client.get('/rp-slash', follow_redirects=False)
        assert r1.status_code == 200

        r2 = await client.get('/rp-api/', follow_redirects=False)
        assert r2.status_code == 200
        assert r2.json() == {'ok': 'api'}


def test_sub_mounts_are_not_rewritten(screen: Screen):
    @ui.page('/')
    def home():
        ui.label('home')

    sub = FastAPI()

    @sub.get('/api')
    def sub_api():
        return {'sub': True}

    app.mount('/sub', sub)

    screen.open('/')
    screen.should_contain('home')

    # calling the non-canonical path must be handled by the mounted sub-app and should redirect
    r = httpx.get(f'http://localhost:{Screen.PORT}/sub/api/', follow_redirects=False)
    assert r.status_code in {301, 307, 308}
    assert r.headers['Location'].endswith('/sub/api')
