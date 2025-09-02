import importlib
from collections.abc import Generator
from copy import copy
from typing import Optional

import pytest
from starlette.routing import Route

import nicegui
from nicegui import Client, app, binding, core, run, ui

# pylint: disable=redefined-outer-name


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addini('main_file', 'main file', default=None)


def get_path_to_main_file(config: pytest.Config) -> Optional[str]:
    main_file = config.getini('main_file')
    if main_file is None:
        main_file = 'main.py'
    if main_file == '':
        return None
    assert config.inipath is not None
    path = (config.inipath.parent / main_file).resolve()
    if not path.is_file():
        return None
    return str(path)


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


def prepare_simulation() -> None:
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
    nicegui.storage.set_storage_secret('simulated secret')
