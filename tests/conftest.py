import importlib
import os
import shutil
from pathlib import Path
from typing import Dict, Generator

import icecream
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from nicegui import Client, binding, globals  # pylint: disable=redefined-builtin
from nicegui.elements import plotly, pyplot
from nicegui.page import page

from .screen import Screen

DOWNLOAD_DIR = Path(__file__).parent / 'download'

icecream.install()


@pytest.fixture
def chrome_options(chrome_options: webdriver.ChromeOptions) -> webdriver.ChromeOptions:
    chrome_options.add_argument('disable-dev-shm-using')
    chrome_options.add_argument('no-sandbox')
    chrome_options.add_argument('headless')
    chrome_options.add_argument('disable-gpu')
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
    capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}
    return capabilities


@pytest.fixture(autouse=True)
def reset_globals() -> Generator[None, None, None]:
    for path in {'/'}.union(globals.page_routes.values()):
        globals.app.remove_route(path)
    globals.app.openapi_schema = None
    globals.app.middleware_stack = None
    globals.app.user_middleware.clear()
    # NOTE favicon routes must be removed separately because they are not "pages"
    for route in globals.app.routes:
        if route.path.endswith('/favicon.ico'):
            globals.app.routes.remove(route)
    importlib.reload(globals)
    # repopulate globals.optional_features
    importlib.reload(plotly)
    importlib.reload(pyplot)
    globals.app.storage.clear()
    globals.index_client = Client(page('/'), shared=True).__enter__()
    globals.app.get('/')(globals.index_client.build_response)
    binding.reset()


@pytest.fixture(scope='session', autouse=True)
def remove_all_screenshots() -> None:
    if os.path.exists(Screen.SCREENSHOT_DIR):
        for name in os.listdir(Screen.SCREENSHOT_DIR):
            os.remove(os.path.join(Screen.SCREENSHOT_DIR, name))


@pytest.fixture(scope='function')
def driver(chrome_options: webdriver.ChromeOptions) -> webdriver.Chrome:
    s = Service()
    driver_ = webdriver.Chrome(service=s, options=chrome_options)
    driver_.implicitly_wait(Screen.IMPLICIT_WAIT)
    driver_.set_page_load_timeout(4)
    yield driver_
    driver_.quit()


@pytest.fixture
def screen(driver: webdriver.Chrome, request: pytest.FixtureRequest, caplog: pytest.LogCaptureFixture) \
        -> Generator[Screen, None, None]:
    screen_ = Screen(driver, caplog)
    yield screen_
    if screen_.is_open:
        screen_.shot(request.node.name)
    logs = screen_.caplog.get_records('call')
    assert not logs, f'There were unexpected logs:\n-------\n{logs}\n-------'
    screen_.stop_server()
    if DOWNLOAD_DIR.exists():
        shutil.rmtree(DOWNLOAD_DIR)
