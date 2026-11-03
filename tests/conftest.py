import os

import pytest
from selenium import webdriver

os.environ.setdefault('MPLBACKEND', 'Agg')  # force a non-GUI Matplotlib backend during tests

pytest_plugins = ['nicegui.testing.plugin']


def pytest_collection_modifyitems(items) -> None:
    for item in items:
        if 'screen' in item.fixturenames:
            item.add_marker('screen')


@pytest.fixture(scope='session')
def nicegui_chrome_options(nicegui_chrome_options: webdriver.ChromeOptions) -> webdriver.ChromeOptions:
    nicegui_chrome_options.add_argument('use-fake-ui-for-media-stream')
    nicegui_chrome_options.add_argument('use-fake-device-for-media-stream')
    return nicegui_chrome_options
