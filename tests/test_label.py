import pytest

from nicegui import ui
from nicegui.testing import Screen


@pytest.fixture(autouse=True)
def enable_csp_for_module(enable_csp):
    """Enable CSP for all tests in this module to verify CSP compatibility."""
    yield


def test_hello_world(screen: Screen):
    @ui.page('/')
    def page():
        ui.label('Hello, world')

    screen.open('/')
    screen.should_contain('Hello, world')


def test_text_0(screen: Screen):
    @ui.page('/')
    def page():
        ui.label(0)

    screen.open('/')
    screen.should_contain('0')
