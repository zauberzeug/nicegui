import datetime
import os
from typing import Callable, Generator

import icecream
import pytest
from justpy.htmlcomponents import JustpyBaseComponent, WebPage
from nicegui import globals
from selenium import webdriver

from .user import User

icecream.install()


@pytest.fixture
def chrome_options(chrome_options: webdriver.ChromeOptions) -> webdriver.ChromeOptions:
    chrome_options.add_argument('headless')
    chrome_options.add_argument('disable-gpu')
    chrome_options.add_argument('window-size=1200x600')
    chrome_options.add_experimental_option('w3c', False)
    return chrome_options


@pytest.fixture
def selenium(selenium: webdriver.Chrome) -> webdriver.Chrome:
    selenium.implicitly_wait(0.1)
    selenium.set_page_load_timeout(1)
    return selenium


@pytest.fixture(autouse=True)
def reset_globals() -> Generator[None, None, None]:
    WebPage.instances = {}
    WebPage.sockets = {}
    WebPage.next_page_id = 0
    JustpyBaseComponent.next_id = 0
    JustpyBaseComponent.instances = {}
    globals.config = None
    globals.server = None
    globals.page_builders = {}
    globals.view_stack = []
    globals.tasks = []
    globals.connect_handlers = []
    globals.disconnect_handlers = []
    globals.startup_handlers = []
    globals.shutdown_handlers = []
    globals.has_auto_index_page = False
    globals.dependencies = {}


@pytest.fixture()
def user(selenium: webdriver.Chrome) -> Generator[User, None, None]:
    user = User(selenium)
    yield user
    user.stop_server()


@pytest.fixture
def screenshot(selenium: webdriver.Chrome) -> Callable[[str], None]:
    # original taken from https://github.com/theserverlessway/pytest-chrome/blob/master/tests/conftest.py
    def shot(name: str = '') -> None:
        directory = 'screenshots'
        if not os.path.exists(directory):
            os.makedirs(directory)
        identifier = datetime.datetime.now().isoformat()
        if name:
            identifier = f'{identifier}-{name}'
        filename = f'{directory}/{identifier}.png'
        print(f'Storing Screenshot to {filename}')
        selenium.get_screenshot_as_file(filename)
    return shot
