import datetime
import importlib
import os
from typing import Callable, Generator

import icecream
import pytest

if True:  # NOTE: prevent formatter from sorting the imports (nicegui must come before justpy)
    from nicegui import ui, globals

from justpy.htmlcomponents import JustpyBaseComponent, WebPage
from selenium import webdriver

from .screen import Screen

icecream.install()


@pytest.fixture
def chrome_options(chrome_options: webdriver.ChromeOptions) -> webdriver.ChromeOptions:
    chrome_options.add_argument('headless')
    chrome_options.add_argument('disable-gpu')
    chrome_options.add_argument('window-size=600x600')
    #chrome_options.add_experimental_option('w3c', False)
    return chrome_options


@pytest.fixture
def capabilities(capabilities):
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


@pytest.fixture()
def screen(selenium: webdriver.Chrome, request: pytest.FixtureRequest) -> Generator[Screen, None, None]:
    name = request.node.name
    os.remove(os.path.join(Screen.SCREENSHOT_DIR, f'{name}.png'))
    screen = Screen(selenium)
    yield screen
    screen.shot(name)
    screen.stop_server()
