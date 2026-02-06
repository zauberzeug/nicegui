import contextlib
import gc
import sys
from copy import copy, deepcopy
from dataclasses import MISSING, fields

from starlette.routing import Route

from .. import app, binding, core, dependencies, event, run, ui
from ..app.app_config import AppConfig
from ..client import Client
from ..logging import log


def _get_default_config_values() -> dict:
    """Get default values for AppConfig fields that can be modified by tests."""
    defaults = {}
    for f in fields(AppConfig):
        if f.name in ('vue_config_script', 'quasar_config'):
            if f.default is not MISSING:
                defaults[f.name] = f.default
            elif f.default_factory is not MISSING:  # type: ignore[comparison-overlap]
                defaults[f.name] = f.default_factory()
    return defaults


_DEFAULT_CONFIG_VALUES = _get_default_config_values()


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
        unocss=None,
        prod_js=True,
        show_welcome_message=False,
    )


@contextlib.contextmanager
def nicegui_reset_globals():
    """Reset the global state of the NiceGUI package."""
    for route in list(app.routes):
        if isinstance(route, Route) and (
            not route.path.startswith('/_nicegui/')
            or route.path.startswith('/_nicegui/auto/static')
            or route.path.startswith('/_nicegui/client/')
        ):
            app.remove_route(route.path)

    app.openapi_schema = None
    app.middleware_stack = None
    app.user_middleware.clear()
    app.urls.clear()
    core.reset()

    element_types: list[type[ui.element]] = [ui.element, *_find_all_subclasses(ui.element)]
    default_classes = {t: copy(t._default_classes) for t in element_types}  # pylint: disable=protected-access
    default_styles = {t: copy(t._default_style) for t in element_types}  # pylint: disable=protected-access
    default_props = {t: copy(t._default_props) for t in element_types}  # pylint: disable=protected-access

    dependencies.importmap_overrides.clear()
    Client.instances.clear()
    Client.page_routes.clear()
    Client.shared_head_html = ''
    Client.shared_body_html = ''
    app.reset()
    binding.reset()

    gc.collect()

    try:
        yield
    finally:
        gc.collect()

        app.reset()
        event.reset()
        run.reset()

        for t in element_types:
            t._default_classes = default_classes[t]  # pylint: disable=protected-access
            t._default_style = default_styles[t]  # pylint: disable=protected-access
            t._default_props = default_props[t]  # pylint: disable=protected-access

        for func in Client.page_routes:
            if not func.__module__.startswith('tests.'):
                parts = func.__module__.split('.')
                for i in range(len(parts)):
                    sys.modules.pop('.'.join(parts[:i+1]), None)  # remove the module and all its parents


def _find_all_subclasses(cls: type) -> list[type]:
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(_find_all_subclasses(subclass))
    return subclasses


def _reset_app_handlers_only() -> None:
    """Reset app handlers without touching the config (for shared server tests)."""
    app.storage.clear()
    app._startup_handlers.clear()  # pylint: disable=protected-access
    app._shutdown_handlers.clear()  # pylint: disable=protected-access
    app._connect_handlers.clear()  # pylint: disable=protected-access
    app._disconnect_handlers.clear()  # pylint: disable=protected-access
    app._delete_handlers.clear()  # pylint: disable=protected-access
    app._exception_handlers[:] = [log.exception]  # pylint: disable=protected-access
    # NOTE: do NOT reset run config fields (title, reload, etc.) as they are needed by the server
    app.colors()  # reset colors to default


def _reset_app_config_modifiable_fields() -> None:
    """Reset config fields that can be modified by tests but don't require server restart."""
    # If run config was lost (e.g., after User fixture reset), restore it
    if not app.config.has_run_config:
        prepare_simulation()
    app.config.vue_config_script = _DEFAULT_CONFIG_VALUES['vue_config_script']
    app.config.quasar_config = deepcopy(_DEFAULT_CONFIG_VALUES['quasar_config'])
    # Reset CSS framework config that tests may have modified
    app.config.unocss = None
    app.config.tailwind = True


@contextlib.contextmanager
def nicegui_reset_globals_for_shared_server():
    """Reset the global state of the NiceGUI package while keeping the server running.

    This is a lighter version of nicegui_reset_globals() that doesn't touch the event loop,
    server instance, or app config, allowing tests to share a single server for faster execution.
    """
    for route in list(app.routes):
        if isinstance(route, Route) and (
            not route.path.startswith('/_nicegui/')
            or route.path.startswith('/_nicegui/auto/static')
            or route.path.startswith('/_nicegui/client/')
        ):
            app.remove_route(route.path)

    app.openapi_schema = None
    app.middleware_stack = None
    app.user_middleware.clear()
    app.urls.clear()
    # NOTE: do NOT call core.reset() as it would clear the event loop

    element_types: list[type[ui.element]] = [ui.element, *_find_all_subclasses(ui.element)]
    default_classes = {t: copy(t._default_classes) for t in element_types}  # pylint: disable=protected-access
    default_styles = {t: copy(t._default_style) for t in element_types}  # pylint: disable=protected-access
    default_props = {t: copy(t._default_props) for t in element_types}  # pylint: disable=protected-access

    dependencies.importmap_overrides.clear()
    # NOTE: do NOT clear Client.instances here as background tasks may still reference them
    # Client cleanup happens naturally when the browser disconnects or navigates away
    Client.page_routes.clear()
    Client.shared_head_html = ''
    Client.shared_body_html = ''
    # NOTE: reset config FIRST, then handlers (which calls app.colors() to set defaults)
    _reset_app_config_modifiable_fields()
    _reset_app_handlers_only()
    binding.reset()

    gc.collect()

    try:
        yield
    finally:
        gc.collect()

        # NOTE: reset config FIRST, then handlers (which calls app.colors() to set defaults)
        _reset_app_config_modifiable_fields()
        _reset_app_handlers_only()
        event.reset()
        # NOTE: do NOT call run.reset() as it would shut down pools used by the running server

        for t in element_types:
            t._default_classes = default_classes[t]  # pylint: disable=protected-access
            t._default_style = default_styles[t]  # pylint: disable=protected-access
            t._default_props = default_props[t]  # pylint: disable=protected-access

        page_routes_snapshot = list(Client.page_routes)  # snapshot to avoid modification during iteration
        for func in page_routes_snapshot:
            if not func.__module__.startswith('tests.'):
                parts = func.__module__.split('.')
                for i in range(len(parts)):
                    sys.modules.pop('.'.join(parts[:i+1]), None)  # remove the module and all its parents
