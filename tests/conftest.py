import datetime
import os

import pytest


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('headless')
    chrome_options.add_argument('disable-gpu')
    chrome_options.add_argument('window-size=1200x600')
    return chrome_options


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(0.1)
    return selenium


# original taken from https://github.com/theserverlessway/pytest-chrome/blob/master/tests/conftest.py
@pytest.fixture
def screenshot(selenium):
    def shot(name=''):
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
