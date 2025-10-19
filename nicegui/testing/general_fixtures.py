import gc
import importlib
import sys
from collections.abc import Generator
from copy import copy
from pathlib import Path
from typing import Optional

import pytest
from starlette.routing import Route

from nicegui import Client, app, binding, core, event, run, ui

# pylint: disable=redefined-outer-name


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add pytest option for main file."""
    parser.addini('main_file', 'main file', default='main.py')


def pytest_configure(config: pytest.Config) -> None:
    """Register the "nicegui_main_file" marker."""
    config.addinivalue_line('markers', 'nicegui_main_file: specify the main file for the test')


def get_path_to_main_file(request: pytest.FixtureRequest) -> Optional[Path]:
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
def nicegui_reset_globals() -> Generator[None, None, None]:
    """Reset the global state of the NiceGUI package."""
    for route in list(app.routes):
        if isinstance(route, Route) and (not route.path.startswith('/_nicegui/') or route.path.startswith('/_nicegui/auto/static')):
            app.remove_route(route.path)

    app.openapi_schema = None
    app.middleware_stack = None
    app.user_middleware.clear()
    app.urls.clear()
    core.air = None
    importlib.reload(core)
    importlib.reload(run)

    # capture initial defaults
    element_types: list[type[ui.element]] = [ui.element, *find_all_subclasses(ui.element)]
    default_classes = {t: copy(t._default_classes) for t in element_types}  # pylint: disable=protected-access
    default_styles = {t: copy(t._default_style) for t in element_types}  # pylint: disable=protected-access
    default_props = {t: copy(t._default_props) for t in element_types}  # pylint: disable=protected-access

    modules_before = set(sys.modules.keys())

    Client.instances.clear()
    Client.page_routes.clear()
    app.reset()
    binding.reset()

    gc.collect()

    yield

    gc.collect()

    app.reset()
    event.reset()

    # restore initial defaults
    for t in element_types:
        t._default_classes = default_classes[t]  # pylint: disable=protected-access
        t._default_style = default_styles[t]  # pylint: disable=protected-access
        t._default_props = default_props[t]  # pylint: disable=protected-access

    modules_after = set(sys.modules.keys())
    # NOTE: remove project modules to ensure @ui.page() decorators run again when main file is re-executed
    for module_name in modules_after - modules_before:
        module = sys.modules.get(module_name)
        if module is None:
            continue
        module_file = getattr(module, '__file__', None)
        if not module_file:
            continue  # NOTE: keep built-in modules like _ast, errno, ...
        module_path = Path(module_file).resolve()
        is_in_site_packages = any(part == 'site-packages' for part in module_path.parts)
        is_in_stdlib = 'lib/python' in str(module_path) and 'site-packages' not in str(module_path)
        if not is_in_site_packages and not is_in_stdlib:
            del sys.modules[module_name]


def find_all_subclasses(cls: type) -> list[type]:
    """Find all subclasses of a class."""
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(find_all_subclasses(subclass))
    return subclasses


def prepare_simulation() -> None:
    """Prepare the simulation by adding the run config and setting the storage secret."""
    core.app.config.add_run_config(
        reload=False,
        title='Test App',
        viewport='',
        favicon=None,
        dark=False,
        language='en-US',
        binding_refresh_interval=0.1,
        reconnect_timeout=3.0,
        message_history_length=1000,
        tailwind=True,
        prod_js=True,
        show_welcome_message=False,
    )
