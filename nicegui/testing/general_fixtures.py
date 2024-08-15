import importlib
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
    element_classes: List[Type[ui.element]] = [ui.element]
    while element_classes:
        parent = element_classes.pop()
        for cls in parent.__subclasses__():
            cls._default_props = {}  # pylint: disable=protected-access
            cls._default_style = {}  # pylint: disable=protected-access
            cls._default_classes = []  # pylint: disable=protected-access
            element_classes.append(cls)
    Client.instances.clear()
    Client.page_routes.clear()
    app.reset()
    Client.auto_index_client = Client(page('/'), request=None).__enter__()  # pylint: disable=unnecessary-dunder-call
    # NOTE we need to re-add the auto index route because we removed all routes above
    app.get('/')(Client.auto_index_client.build_response)
    binding.reset()
    yield


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
        tailwind=True,
        prod_js=True,
        show_welcome_message=False,
    )
    nicegui.storage.set_storage_secret('simulated secret')
