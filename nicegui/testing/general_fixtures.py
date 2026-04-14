import os
import shutil
import tempfile
from pathlib import Path

import pytest

# Set up session-unique storage directory BEFORE importing nicegui modules.
# This ensures Storage.path reads the correct env var during class definition.
_nicegui_storage_dir = tempfile.mkdtemp(prefix='nicegui-test-storage-')
os.environ['NICEGUI_STORAGE_PATH'] = _nicegui_storage_dir

from . import general  # noqa: E402  # must be after env var setup

# pylint: disable=redefined-outer-name


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add pytest option for main file."""
    parser.addini('main_file', 'main file', default='main.py')


def pytest_configure(config: pytest.Config) -> None:
    """Register the "nicegui_main_file" marker and set up session-unique storage path."""
    config.addinivalue_line('markers', 'nicegui_main_file: specify the main file for the test')

    # Also update Storage.path directly in case the class was already imported
    # before the env var was set (nicegui/__init__.py imports storage early).
    from ..storage import Storage  # pylint: disable=import-outside-toplevel
    Storage.path = Path(_nicegui_storage_dir).resolve()


def pytest_unconfigure(config: pytest.Config) -> None:
    """Clean up session-unique storage directory."""
    if _nicegui_storage_dir:
        shutil.rmtree(_nicegui_storage_dir, ignore_errors=True)


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
