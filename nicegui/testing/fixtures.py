import asyncio
import importlib
import os
import shutil
from pathlib import Path
from typing import AsyncGenerator, Callable, Dict, Generator, List, Type

import httpx
import icecream
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from starlette.routing import Route

import nicegui.storage
from nicegui import Client, app, binding, core, run, ui
from nicegui.functions.navigate import Navigate
from nicegui.page import page

from .screen import Screen
from .user import User

# pylint: disable=redefined-outer-name

DOWNLOAD_DIR = Path(__file__).parent / 'download'

icecream.install()


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line('markers',
                            'module_under_test: specify the module under test which then gets automatically reloaded.')


@pytest.fixture
def nicegui_chrome_options(chrome_options: webdriver.ChromeOptions) -> webdriver.ChromeOptions:
    chrome_options.add_argument('disable-dev-shm-usage')
    chrome_options.add_argument('no-sandbox')
    chrome_options.add_argument('headless')
    chrome_options.add_argument('disable-gpu' if 'GITHUB_ACTIONS' in os.environ else '--use-gl=angle')
    chrome_options.add_argument('window-size=600x600')
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': str(DOWNLOAD_DIR),
        'download.prompt_for_download': False,  # To auto download the file
        'download.directory_upgrade': True,
    })
    if 'CHROME_BINARY_LOCATION' in os.environ:
        chrome_options.binary_location = os.environ['CHROME_BINARY_LOCATION']
    return chrome_options


@pytest.fixture
def capabilities(capabilities: Dict) -> Dict:
    """Configure the Chrome driver capabilities."""
    capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}
    return capabilities


@pytest.fixture
def nicegui_reset_globals() -> Generator[None, None, None]:
    """Reset the global state of the NiceGUI package."""
    for route in app.routes:
        if isinstance(route, Route) and route.path.startswith('/_nicegui/auto/static/'):
            app.remove_route(route.path)
    for path in {'/'}.union(Client.page_routes.values()):
        app.remove_route(path)
    app.openapi_schema = None
    app.middleware_stack = None
    app.user_middleware.clear()
    app.urls.clear()
    core.air = None
    # NOTE favicon routes must be removed separately because they are not "pages"
    for route in app.routes:
        if isinstance(route, Route) and route.path.endswith('/favicon.ico'):
            app.routes.remove(route)
    importlib.reload(core)
    importlib.reload(run)
    element_classes: List[Type[ui.element]] = [ui.element]
    while element_classes:
        parent = element_classes.pop()
        for cls in parent.__subclasses__():
            cls._default_props = {}  # pylint: disable=protected-access
            cls._default_style = {}  # pylint: disable=protected-access
            cls._default_classes = []  # pylint: disable=protected-access
            element_classes.append(cls)
    Client.instances.clear()
    Client.page_routes.clear()
    app.reset()
    Client.auto_index_client = Client(page('/'), request=None).__enter__()  # pylint: disable=unnecessary-dunder-call
    # NOTE we need to re-add the auto index route because we removed all routes above
    app.get('/')(Client.auto_index_client.build_response)
    binding.reset()
    yield


@pytest.fixture(scope='session')
def nicegui_remove_all_screenshots() -> None:
    """Remove all screenshots from the screenshot directory before the test session."""
    if os.path.exists(Screen.SCREENSHOT_DIR):
        for name in os.listdir(Screen.SCREENSHOT_DIR):
            os.remove(os.path.join(Screen.SCREENSHOT_DIR, name))


@pytest.fixture()
def nicegui_driver(nicegui_chrome_options: webdriver.ChromeOptions) -> Generator[webdriver.Chrome, None, None]:
    """Create a new Chrome driver instance."""
    s = Service()
    driver_ = webdriver.Chrome(service=s, options=nicegui_chrome_options)
    driver_.implicitly_wait(Screen.IMPLICIT_WAIT)
    driver_.set_page_load_timeout(4)
    yield driver_
    driver_.quit()


@pytest.fixture
def screen(nicegui_reset_globals,
           nicegui_remove_all_screenshots,
           nicegui_driver: webdriver.Chrome,
           request: pytest.FixtureRequest,
           caplog: pytest.LogCaptureFixture,
           ) -> Generator[Screen, None, None]:
    """Create a new SeleniumScreen fixture."""
    screen_ = Screen(nicegui_driver, caplog)
    yield screen_
    logs = screen_.caplog.get_records('call')
    if screen_.is_open:
        screen_.shot(request.node.name)
    screen_.stop_server()
    if DOWNLOAD_DIR.exists():
        shutil.rmtree(DOWNLOAD_DIR)
    if logs:
        pytest.fail('There were unexpected logs. See "Captured log call" below.', pytrace=False)


@pytest.fixture
async def user(nicegui_reset_globals, prepare_simulated_auto_index_client, request: pytest.FixtureRequest) -> AsyncGenerator[User, None]:
    """Create a new user fixture."""
    prepare_simulation(request)
    async with core.app.router.lifespan_context(core.app):
        async with httpx.AsyncClient(app=core.app, base_url='http://test') as client:
            yield User(client)
    ui.navigate = Navigate()


@pytest.fixture
async def create_user(nicegui_reset_globals, prepare_simulated_auto_index_client, request: pytest.FixtureRequest) -> AsyncGenerator[Callable[[], User], None]:
    """Create a fixture for building new users."""
    prepare_simulation(request)
    async with core.app.router.lifespan_context(core.app):
        yield lambda: User(httpx.AsyncClient(app=core.app, base_url='http://test'))
    ui.navigate = Navigate()


@pytest.fixture()
def prepare_simulated_auto_index_client(request):
    original_test = request.node._obj  # pylint: disable=protected-access
    if asyncio.iscoroutinefunction(original_test):
        async def wrapped_test(*args, **kwargs):
            with Client.auto_index_client:
                return await original_test(*args, **kwargs)
        request.node._obj = wrapped_test  # pylint: disable=protected-access
    else:
        def wrapped_test(*args, **kwargs):
            Client.auto_index_client.__enter__()
            return original_test(*args, **kwargs)
        request.node._obj = wrapped_test  # pylint: disable=protected-access


def prepare_simulation(request: pytest.FixtureRequest) -> None:
    """Prepare a simulation to be started -- by using the "module_under_test" marker you can specify the main entry point of the app."""
    marker = request.node.get_closest_marker('module_under_test')
    if marker is not None:
        with Client.auto_index_client:
            importlib.reload(marker.args[0])

    core.app.config.add_run_config(
        reload=False,
        title='Test App',
        viewport='',
        favicon=None,
        dark=False,
        language='en-US',
        binding_refresh_interval=0.1,
        reconnect_timeout=3.0,
        tailwind=True,
        prod_js=True,
        show_welcome_message=False,
    )
    nicegui.storage.set_storage_secret('simulated secret')
