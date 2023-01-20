import importlib
import os
from typing import Dict, Generator

import icecream
import pytest
from selenium import webdriver

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


@pytest.fixture
def selenium(selenium: webdriver.Chrome) -> webdriver.Chrome:
    selenium.implicitly_wait(2)
    selenium.set_page_load_timeout(2)
    return selenium


@pytest.fixture(autouse=True)
def reset_globals() -> Generator[None, None, None]:
    for path in {'/'}.union(globals.page_routes.values()):
        globals.app.remove_route(path)
    importlib.reload(globals)
    globals.index_client = Client(page('/'), shared=True).__enter__()
    globals.app.get('/')(globals.index_client.build_response)


@pytest.fixture(scope='session', autouse=True)
def remove_all_screenshots() -> None:
    if os.path.exists(Screen.SCREENSHOT_DIR):
        for name in os.listdir(Screen.SCREENSHOT_DIR):
            os.remove(os.path.join(Screen.SCREENSHOT_DIR, name))


@pytest.fixture
def screen(selenium: webdriver.Chrome, request: pytest.FixtureRequest, caplog: pytest.LogCaptureFixture) \
        -> Generator[Screen, None, None]:
    screen = Screen(selenium, caplog)
    yield screen
    if screen.is_open:
        screen.shot(request.node.name)
    logs = screen.caplog.get_records('call')
    assert not logs, f'There were unexpected logs:\n-------\n{logs}\n-------'
    screen.stop_server()
