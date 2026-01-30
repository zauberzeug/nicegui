import contextlib
import gc
import sys
from copy import copy

from starlette.routing import Route

from .. import app, binding, core, dependencies, event, run, ui
from ..client import Client


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
