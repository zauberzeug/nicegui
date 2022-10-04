import importlib
import os
from typing import Dict, Generator

import icecream
import pytest

if True:  # NOTE: prevent formatter from sorting the imports (NiceGUI must come before JustPy)
    from nicegui import globals

from justpy.htmlcomponents import JustpyBaseComponent, WebPage
from selenium import webdriver

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
    selenium.implicitly_wait(0.5)
    selenium.set_page_load_timeout(2)
    return selenium


@pytest.fixture(autouse=True)
def reset_globals() -> Generator[None, None, None]:
    WebPage.sockets.clear()
    WebPage.instances.clear()
    WebPage.next_page_id = 0
    JustpyBaseComponent.instances.clear()
    JustpyBaseComponent.next_id = 0
    importlib.reload(globals)


@pytest.fixture(scope='session', autouse=True)
def remove_all_screenshots() -> None:
    if os.path.exists(Screen.SCREENSHOT_DIR):
        for name in os.listdir(Screen.SCREENSHOT_DIR):
            os.remove(os.path.join(Screen.SCREENSHOT_DIR, name))


@pytest.fixture
def screen(selenium: webdriver.Chrome, request: pytest.FixtureRequest) -> Generator[Screen, None, None]:
    screen = Screen(selenium)
    yield screen
    screen.shot(request.node.name)
    screen.stop_server()
