from pathlib import Path

import pytest

from . import general

# pylint: disable=redefined-outer-name


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add pytest option for main file."""
    parser.addini('main_file', 'main file', default='main.py')


def pytest_configure(config: pytest.Config) -> None:
    """Register the "nicegui_main_file" marker."""
    config.addinivalue_line('markers', 'nicegui_main_file: specify the main file for the test')


def get_path_to_main_file(request: pytest.FixtureRequest) -> Path | None:
    """Get the path to the main file from the test marker or global config."""
    marker = next((m for m in request.node.iter_markers('nicegui_main_file')), None)
    main_file = marker.args[0] if marker else request.config.getini('main_file')
    if not main_file:
        return None
    assert request.config.inipath is not None
    path = (request.config.inipath.parent / main_file).resolve()
    if not path.is_file():
        raise FileNotFoundError(f'Main file not found: {path}')
    return path


@pytest.fixture
def nicegui_reset_globals():
    """Reset the global state of the NiceGUI package."""
    with general.nicegui_reset_globals():
        yield


@pytest.fixture
def enable_csp():
    """Enable CSP for a specific test to verify CSP-compatible functionality.

    By default, CSP is disabled in tests because many NiceGUI features (like ui.add_css())
    use dynamic style injection which is incompatible with strict CSP. Use this fixture
    for tests that verify core functionality works with CSP enabled.

    Example:
        def test_basic_elements(screen: Screen, enable_csp):
            # Test that basic UI elements work with CSP
            @ui.page('/')
            def page():
                ui.label('Test')
                ui.button('Click me')
            screen.open('/')
            screen.should_contain('Test')
    """
    from .. import core
    original_value = core.app.config.csp_enabled
    core.app.config.csp_enabled = True
    yield
    core.app.config.csp_enabled = original_value
