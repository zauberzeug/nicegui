import shutil
import tempfile
from pathlib import Path

import pytest

from . import general

# pylint: disable=redefined-outer-name

_nicegui_storage_dir: str | None = None


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add pytest option for main file."""
    parser.addini('main_file', 'main file', default='main.py')


def pytest_configure(config: pytest.Config) -> None:
    """Register the "nicegui_main_file" marker and set up a session-unique storage path."""
    config.addinivalue_line('markers', 'nicegui_main_file: specify the main file for the test')

    global _nicegui_storage_dir  # pylint: disable=global-statement # noqa: PLW0603
    _nicegui_storage_dir = tempfile.mkdtemp(prefix='nicegui-test-storage-')

    from .. import app  # pylint: disable=import-outside-toplevel
    from ..storage import Storage  # pylint: disable=import-outside-toplevel
    Storage.path = Path(_nicegui_storage_dir).resolve()
    # Rebuild app.storage once so its FilePersistentDict picks up the new path
    # (the instance constructed at App.__init__ captured the default path).
    # Safe here: app.start() has not run yet, so no shutdown hook is bound to the old instance.
    app.storage = Storage()


def pytest_unconfigure(config: pytest.Config) -> None:  # pylint: disable=unused-argument
    """Clean up session-unique storage directory."""
    if _nicegui_storage_dir is not None:
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
