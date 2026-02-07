"""Tests to verify basic functionality works with CSP enabled."""
import pytest

from nicegui import ui
from nicegui.testing import Screen


@pytest.fixture(autouse=True)
def enable_csp_for_module(enable_csp):
    """Enable CSP for all tests in this module to verify CSP compatibility."""
    yield


def test_basic_elements(screen: Screen) -> None:
    """Test that basic UI elements work with CSP enabled."""
    @ui.page('/')
    def page():
        ui.label('Hello CSP!').classes('test-label')
        ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))
        with ui.row():
            ui.label('Row 1')
            ui.label('Row 2')

    screen.open('/')
    screen.should_contain('Hello CSP!')
    screen.should_contain('Click me')
    screen.click('Click me')
    screen.should_contain('Clicked!')


def test_static_styles(screen: Screen) -> None:
    """Test that static CSS classes work with CSP enabled."""
    @ui.page('/')
    def page():
        # Using Tailwind classes works fine with CSP
        ui.label('Red text').classes('text-red-500')
        ui.label('Bold text').classes('font-bold')
        ui.button('Primary').classes('bg-blue-500')

    screen.open('/')
    screen.should_contain('Red text')
    screen.should_contain('Bold text')


def test_static_head_html(screen: Screen) -> None:
    """Test that static HTML added during page build works with CSP."""
    @ui.page('/')
    def page():
        # Static HTML added during page build gets nonces injected automatically
        ui.add_head_html('<style>.csp-works {color: green; font-weight: bold;}</style>')
        ui.label('CSP Compatible!').classes('csp-works')

    screen.open('/')
    label = screen.find('CSP Compatible!')
    # The style should be applied
    assert label.value_of_css_property('color') == 'rgba(0, 128, 0, 1)'
    assert label.value_of_css_property('font-weight') == '700'


def test_page_title_and_meta(screen: Screen) -> None:
    """Test that page metadata works with CSP enabled."""
    @ui.page('/', title='CSP Test Page', favicon='🔒')
    def page():
        ui.label('Secure page')

    screen.open('/')
    screen.should_contain('Secure page')
