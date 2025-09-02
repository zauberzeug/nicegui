import importlib
from collections.abc import Generator
from copy import copy
from pathlib import Path

import pytest
from starlette.routing import Route

from nicegui import Client, app, binding, core, run, ui

# pylint: disable=redefined-outer-name


def pytest_configure(config: pytest.Config) -> None:
    """Add the "module_under_test" marker to the pytest configuration."""
    config.addinivalue_line('markers',
                            'module_under_test(module): specify the module under test which then gets automatically reloaded.')


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addini('main_file', 'main file', default='main.py')


def resolve_main_path(config: pytest.Config) -> str:
    main_file = config.getini('main_file')
    ini_path = config.inipath
    if ini_path:
        ini_dir = ini_path.parent
    else:
        root = getattr(config, 'rootpath', None)
        ini_dir = Path(root) if root is not None else Path.cwd()
    main_path = Path(main_file)
    if not main_path.is_absolute():
        main_path = ini_dir / main_path
    return str(main_path)


@pytest.fixture
def nicegui_reset_globals() -> Generator[None, None, None]:
    """Reset the global state of the NiceGUI package."""
    for route in list(app.routes):
        if isinstance(route, Route) and route.path.startswith('/_nicegui/auto/static/'):
            app.remove_route(route.path)

    all_page_routes = set(Client.page_routes.values())
    all_page_routes.add('/')
    for path in all_page_routes:
        app.remove_route(path)

    for route in list(app.routes):
        if (
            isinstance(route, Route) and
            '{' in route.path and '}' in route.path and
            not route.path.startswith('/_nicegui/')
        ):
            app.remove_route(route.path)

    app.openapi_schema = None
    app.middleware_stack = None
    app.user_middleware.clear()
    app.urls.clear()
    core.air = None
    # NOTE favicon routes must be removed separately because they are not "pages"
    for route in list(app.routes):
        if isinstance(route, Route) and route.path.endswith('/favicon.ico'):
            app.routes.remove(route)
    importlib.reload(core)
    importlib.reload(run)

    # capture initial defaults
    element_types: list[type[ui.element]] = [ui.element, *find_all_subclasses(ui.element)]
    default_classes = {t: copy(t._default_classes) for t in element_types}  # pylint: disable=protected-access
    default_styles = {t: copy(t._default_style) for t in element_types}  # pylint: disable=protected-access
    default_props = {t: copy(t._default_props) for t in element_types}  # pylint: disable=protected-access

    Client.instances.clear()
    Client.page_routes.clear()
    app.reset()
    binding.reset()

    yield

    app.reset()

    # restore initial defaults
    for t in element_types:
        t._default_classes = default_classes[t]  # pylint: disable=protected-access
        t._default_style = default_styles[t]  # pylint: disable=protected-access
        t._default_props = default_props[t]  # pylint: disable=protected-access


def find_all_subclasses(cls: type) -> list[type]:
    """Find all subclasses of a class."""
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(find_all_subclasses(subclass))
    return subclasses
