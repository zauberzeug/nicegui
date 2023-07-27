import importlib
import os
from typing import Dict, Generator

import icecream
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from nicegui import Client, globals
from nicegui.page import page

from .screen import Screen

icecream.install()


@pytest.fixture
def chrome_options(chrome_options: webdriver.ChromeOptions) -> webdriver.ChromeOptions:
    chrome_options.add_argument('headless')
    chrome_options.add_argument('disable-gpu')
    chrome_options.add_argument('window-size=600x600')
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
    [globals.app.routes.remove(r) for r in globals.app.routes if r.path.endswith('/favicon.ico')]
    importlib.reload(globals)
    globals.app.storage.clear()
    globals.index_client = Client(page('/'), shared=True).__enter__()
    globals.app.get('/')(globals.index_client.build_response)


@pytest.fixture(scope='session', autouse=True)
def remove_all_screenshots() -> None:
    if os.path.exists(Screen.SCREENSHOT_DIR):
        for name in os.listdir(Screen.SCREENSHOT_DIR):
            os.remove(os.path.join(Screen.SCREENSHOT_DIR, name))


@pytest.fixture(scope='function')
def driver(chrome_options: webdriver.ChromeOptions) -> webdriver.Chrome:
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.implicitly_wait(Screen.IMPLICIT_WAIT)
    driver.set_page_load_timeout(4)
    yield driver
    driver.quit()


@pytest.fixture
def screen(driver: webdriver.Chrome, request: pytest.FixtureRequest, caplog: pytest.LogCaptureFixture) \
        -> Generator[Screen, None, None]:
    screen = Screen(driver, caplog)
    yield screen
    if screen.is_open:
        screen.shot(request.node.name)
    logs = screen.caplog.get_records('call')
    assert not logs, f'There were unexpected logs:\n-------\n{logs}\n-------'
    screen.stop_server()
