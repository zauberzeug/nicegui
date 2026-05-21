import atexit
import os
import shutil
import tempfile
from pathlib import Path

import pytest

from .. import app
from ..storage import Storage
from . import general

# pylint: disable=redefined-outer-name


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add pytest option for main file."""
    parser.addini('main_file', 'main file', default='main.py')


def pytest_configure(config: pytest.Config) -> None:
    """Set up a session-unique storage path and register the "nicegui_main_file" marker."""
    if Storage.path != Path(os.environ.get('NICEGUI_STORAGE_PATH', '.nicegui')).resolve():
        return  # already configured

    Storage.path = Path(tempfile.mkdtemp(prefix='nicegui-test-storage-')).resolve()
    atexit.register(shutil.rmtree, Storage.path, ignore_errors=True)
    app.storage = Storage()  # rebuild app.storage so its FilePersistentDict picks up the new path
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
