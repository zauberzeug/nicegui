import importlib
from copy import copy
from typing import Generator, List, Type

import pytest
from starlette.routing import Route

import nicegui.storage
from nicegui import Client, app, binding, core, run, ui
from nicegui.page import page

# pylint: disable=redefined-outer-name


def pytest_configure(config: pytest.Config) -> None:
    """Add the "module_under_test" marker to the pytest configuration."""
    config.addinivalue_line('markers',
                            'module_under_test(module): specify the module under test which then gets automatically reloaded.')


@pytest.fixture
def nicegui_reset_globals() -> Generator[None, None, None]:
    """Reset the global state of the NiceGUI package."""
    for route in app.routes:
        if isinstance(route, Route) and route.path.startswith('/_nicegui/auto/static/'):
            app.remove_route(route.path)
    for path in {'/'}.union(Client.page_routes.values()):
        app.remove_route(path)
    app.openapi_schema = None
    app.middleware_stack = None
    app.user_middleware.clear()
    app.urls.clear()
    core.air = None
    # NOTE favicon routes must be removed separately because they are not "pages"
    for route in app.routes:
        if isinstance(route, Route) and route.path.endswith('/favicon.ico'):
            app.routes.remove(route)
    importlib.reload(core)
    importlib.reload(run)

    # capture initial defaults
    element_types: List[Type[ui.element]] = [ui.element, *find_all_subclasses(ui.element)]
    default_classes = {t: copy(t._default_classes) for t in element_types}  # pylint: disable=protected-access
    default_styles = {t: copy(t._default_style) for t in element_types}  # pylint: disable=protected-access
    default_props = {t: copy(t._default_props) for t in element_types}  # pylint: disable=protected-access

    Client.instances.clear()
    Client.page_routes.clear()
    app.reset()
    Client.auto_index_client = Client(page('/'), request=None).__enter__()  # pylint: disable=unnecessary-dunder-call
    # NOTE we need to re-add the auto index route because we removed all routes above
    app.get('/')(Client.auto_index_client.build_response)
    binding.reset()

    yield

    app.reset()

    # restore initial defaults
    for t in element_types:
        t._default_classes = default_classes[t]  # pylint: disable=protected-access
        t._default_style = default_styles[t]  # pylint: disable=protected-access
        t._default_props = default_props[t]  # pylint: disable=protected-access


def find_all_subclasses(cls: Type) -> List[Type]:
    """Find all subclasses of a class."""
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(find_all_subclasses(subclass))
    return subclasses


def prepare_simulation(request: pytest.FixtureRequest) -> None:
    """Prepare a simulation to be started.

    By using the "module_under_test" marker you can specify the main entry point of the app.
    """
    marker = request.node.get_closest_marker('module_under_test')
    if marker is not None:
        with Client.auto_index_client:
            importlib.reload(marker.args[0])

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
