import asyncio
import importlib
import os
import shutil
from pathlib import Path
from typing import Dict, Generator, Union, get_type_hints

import httpx
import icecream
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from starlette.routing import Route

from nicegui import Client, app, binding, core
from nicegui.page import page

from .selenium_screen import SeleniumScreen
from .simulated_screen import SimulatedScreen

# pylint: disable=redefined-outer-name

DOWNLOAD_DIR = Path(__file__).parent / 'download'

icecream.install()


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "module_under_test: specify the module under test which then get's automatically reloaded.")


@pytest.fixture
def nicegui_chrome_options(chrome_options: webdriver.ChromeOptions) -> webdriver.ChromeOptions:
    """Configure the Chrome driver options."""
    chrome_options.add_argument('disable-dev-shm-using')
    chrome_options.add_argument('no-sandbox')
    chrome_options.add_argument('headless')
    # check if we are running on GitHub Actions
    if 'GITHUB_ACTIONS' in os.environ:
        chrome_options.add_argument('disable-gpu')
    else:
        chrome_options.add_argument('--use-gl=angle')
    chrome_options.add_argument('window-size=600x600')
    chrome_options.add_experimental_option('prefs', {
        "download.default_directory": str(DOWNLOAD_DIR),
        "download.prompt_for_download": False,  # To auto download the file
        "download.directory_upgrade": True,
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
    # NOTE favicon routes must be removed separately because they are not "pages"
    for route in app.routes:
        if isinstance(route, Route) and route.path.endswith('/favicon.ico'):
            app.routes.remove(route)
    importlib.reload(core)
    Client.instances.clear()
    Client.page_routes.clear()
    app.reset()
    Client.auto_index_client = Client(page('/'), shared=True).__enter__()  # pylint: disable=unnecessary-dunder-call
    # NOTE we need to re-add the auto index route because we removed all routes above
    app.get('/')(Client.auto_index_client.build_response)
    binding.reset()
    yield


@pytest.fixture(scope='session')
def nicegui_remove_all_screenshots() -> None:
    """Remove all screenshots from the screenshot directory before the test session."""
    if os.path.exists(SeleniumScreen.SCREENSHOT_DIR):
        for name in os.listdir(SeleniumScreen.SCREENSHOT_DIR):
            os.remove(os.path.join(SeleniumScreen.SCREENSHOT_DIR, name))


@pytest.fixture()
def nicegui_driver(nicegui_chrome_options: webdriver.ChromeOptions) -> Generator[webdriver.Chrome, None, None]:
    """Create a new Chrome driver instance."""
    s = Service()
    driver_ = webdriver.Chrome(service=s, options=nicegui_chrome_options)
    driver_.implicitly_wait(SeleniumScreen.IMPLICIT_WAIT)
    driver_.set_page_load_timeout(4)
    yield driver_
    driver_.quit()


@pytest.fixture
def screen(nicegui_reset_globals, request: pytest.FixtureRequest) -> Generator[Union[SeleniumScreen, SimulatedScreen], None, None]:
    """Create a new Screen fixture."""
    screen_type_hint = get_type_hints(request.node.function).get('screen')
    assert isinstance(screen_type_hint, type)
    if issubclass(screen_type_hint, SimulatedScreen):
        yield request.getfixturevalue('simulated_screen')
    elif issubclass(screen_type_hint, SeleniumScreen):
        yield request.getfixturevalue('selenium_screen')
    else:
        raise ValueError(f'Unknown screen type: {screen_type_hint}, expected Screen or SimulatedScreen.')


@pytest.fixture
def selenium_screen(nicegui_remove_all_screenshots,
                    nicegui_driver: webdriver.Chrome,
                    request: pytest.FixtureRequest,
                    caplog: pytest.LogCaptureFixture,
                    ) -> Generator[SeleniumScreen, None, None]:
    """Create a new SeleniumScreen fixture."""
    screen = SeleniumScreen(nicegui_driver, caplog)
    yield screen
    if screen.is_open:
        screen.shot(request.node.name)
    logs = screen.caplog.get_records('call')
    screen.stop_server()
    if DOWNLOAD_DIR.exists():
        shutil.rmtree(DOWNLOAD_DIR)
    if logs:
        pytest.fail('There were unexpected logs. See "Captured log call" below.', pytrace=False)


@pytest.fixture
async def simulated_screen(request: pytest.FixtureRequest) -> Generator[SimulatedScreen, None, None]:
    """Create a new SimulatedScreen fixture."""
    marker = request.node.get_closest_marker('module_under_test')
    if marker is not None:
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
    async with core.app.router.lifespan_context(core.app):
        async with httpx.AsyncClient(app=core.app, base_url='http://test') as client:
            yield SimulatedScreen(client)
