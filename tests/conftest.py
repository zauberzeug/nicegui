import os

from nicegui.testing import Screen

os.environ.setdefault('MPLBACKEND', 'Agg')  # force a non-GUI Matplotlib backend during tests

pytest_plugins = ['nicegui.testing.plugin']

Screen.SCREENSHOT_PASSED_TESTS = False  # screenshots of failed tests suffice and save time


def pytest_collection_modifyitems(items) -> None:
    for item in items:
        if 'screen' in item.fixturenames:
            item.add_marker('screen')
