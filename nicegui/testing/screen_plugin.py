import os
import shutil
from collections.abc import Generator
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from .general_fixtures import (  # noqa: F401  # pylint: disable=unused-import
    nicegui_reset_globals,
    pytest_addoption,
    pytest_configure,
)
from .screen import Screen

# pylint: disable=redefined-outer-name

DOWNLOAD_DIR = Path(__file__).parent / 'download'


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):  # pylint: disable=unused-argument
    """Store test outcome in the node for fixture access."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f'rep_{rep.when}', rep)


@pytest.fixture
def nicegui_chrome_options(chrome_options: webdriver.ChromeOptions) -> webdriver.ChromeOptions:
    """Configure the Chrome options for the NiceGUI tests."""
    chrome_options.add_argument('disable-dev-shm-usage')
    chrome_options.add_argument('disable-search-engine-choice-screen')
    chrome_options.add_argument('no-sandbox')
    chrome_options.add_argument('headless')
    if 'GITHUB_ACTIONS' in os.environ:
        chrome_options.add_argument('disable-gpu')
        chrome_options.add_argument('enable-unsafe-swiftshader')
    else:
        chrome_options.add_argument('--use-gl=angle')
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
def capabilities(capabilities: dict) -> dict:
    """Configure the Chrome driver capabilities."""
    capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}
    return capabilities


@pytest.fixture(scope='session')
def nicegui_remove_all_screenshots() -> None:
    """Remove all screenshots from the screenshot directory before the test session."""
    for name in Screen.SCREENSHOT_DIR.glob('*.png'):
        name.unlink()


@pytest.fixture()
def nicegui_driver(nicegui_chrome_options: webdriver.ChromeOptions) -> Generator[webdriver.Chrome, None, None]:
    """Create a new Chrome driver instance."""
    for executable_path in (None, shutil.which('chromedriver'), 'chromedriver'):  # Required for ARM devcontainers
        try:
            s = Service(executable_path=executable_path)
            driver_ = webdriver.Chrome(service=s, options=nicegui_chrome_options)
            break
        except Exception:
            continue
    else:  # no break
        raise RuntimeError('Could not start Chrome WebDriver.')
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
    os.environ['NICEGUI_SCREEN_TEST_PORT'] = str(Screen.PORT)
    screen_ = Screen(nicegui_driver, caplog, request)
    try:
        yield screen_

        logs = [record for record in screen_.caplog.get_records('call') if record.levelname == 'ERROR']
        if screen_.is_open:
            test_failed = hasattr(request.node, 'rep_call') and request.node.rep_call.failed
            screen_.shot(request.node.name, failed=test_failed or bool(logs))
        if logs:
            pytest.fail('There were unexpected ERROR logs.', pytrace=False)
        if screen_.is_open and Screen.CATCH_JS_ERRORS:
            for js_error in screen_.selenium.get_log('browser'):
                if str(js_error.get('level', '')).upper() in ('SEVERE', 'ERROR') and \
                        not any(allowed_error in js_error['message'] for allowed_error in screen_.allowed_js_errors):
                    pytest.fail(f'JavaScript console error:\n{js_error}', pytrace=False)
    finally:
        os.environ.pop('NICEGUI_SCREEN_TEST_PORT', None)
        screen_.stop_server()
        if DOWNLOAD_DIR.exists():
            shutil.rmtree(DOWNLOAD_DIR)
