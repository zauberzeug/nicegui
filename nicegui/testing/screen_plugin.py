import os
import shutil
from pathlib import Path
from typing import Dict, Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from .general_fixtures import (  # noqa: F401  # pylint: disable=unused-import
    nicegui_reset_globals,
    prepare_simulation,
    pytest_configure,
)
from .screen import Screen

# pylint: disable=redefined-outer-name

DOWNLOAD_DIR = Path(__file__).parent / 'download'


@pytest.fixture
def nicegui_chrome_options(chrome_options: webdriver.ChromeOptions) -> webdriver.ChromeOptions:
    """Configure the Chrome options for the NiceGUI tests."""
    chrome_options.add_argument('disable-dev-shm-usage')
    chrome_options.add_argument('disable-search-engine-choice-screen')
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
def screen(nicegui_reset_globals,  # noqa: F811, pylint: disable=unused-argument
           nicegui_remove_all_screenshots,  # pylint: disable=unused-argument
           nicegui_driver: webdriver.Chrome,
           request: pytest.FixtureRequest,
           caplog: pytest.LogCaptureFixture,
           ) -> Generator[Screen, None, None]:
    """Create a new SeleniumScreen fixture."""
    prepare_simulation(request)
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
