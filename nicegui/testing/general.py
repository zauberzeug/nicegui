import contextlib
import gc
import sys
from copy import copy

from fastapi.dependencies import models as fastapi_dependency_models
from starlette.routing import Route

from .. import app, background_tasks, binding, core, dependencies, event, run, ui
from ..client import Client
from ..helpers import warnings
from ..slot import Slot


def prepare_simulation() -> None:
    """Prepare the simulation by adding the run config and setting the storage secret."""
    core.app.config.add_run_config(
        reload=False,
        title='Test App',
        viewport='',
        favicon=None,
        dark=False,
        language=None,
        binding_refresh_interval=0.1,
        reconnect_timeout=3.0,
        message_history_length=1000,
        tailwind=True,
        unocss=None,
        prod_js=True,
        show_welcome_message=False,
        markdown=False,
    )


@contextlib.contextmanager
def nicegui_reset_globals():
    """Reset the global state of the NiceGUI package."""
    for route in list(app.routes):
        if isinstance(route, Route) and (
            not route.path.startswith('/_nicegui/')
            or route.path.startswith('/_nicegui/auto/')
        ):
            app.remove_route(route.path)
        if hasattr(route, 'original_router'):  # a router that FastAPI keeps as a single lazy route
            app.routes.remove(route)

    # FastAPI caches callables like page functions with strong references, which would keep them alive across tests
    for name in ('_is_gen_callable_cached', '_is_async_gen_callable_cached', '_is_coroutine_callable_cached'):
        cached_function = getattr(fastapi_dependency_models, name, None)
        if cached_function is not None:
            cached_function.cache_clear()

    app.openapi_schema = None
    app.middleware_stack = None
    app.user_middleware.clear()
    app.urls.clear()
    core.reset()

    element_types: list[type[ui.element]] = [ui.element, *_find_all_subclasses(ui.element)]
    default_classes = {t: copy(t._default_classes) for t in element_types}  # pylint: disable=protected-access
    default_styles = {t: copy(t._default_style) for t in element_types}  # pylint: disable=protected-access
    default_props = {t: copy(t._default_props) for t in element_types}  # pylint: disable=protected-access
    default_markdown_extras = ui.markdown.default_extras[:]

    dependencies.importmap_overrides.clear()
    Client.instances.clear()
    Slot.stacks.clear()
    Client.page_routes.clear()
    Client.shared_head_html = ''
    Client.shared_body_html = ''
    app.reset()
    background_tasks.reset()
    binding.reset()
    warnings.reset()

    gc.collect()

    try:
        yield
    finally:
        gc.collect()

        app.reset()
        background_tasks.reset()
        event.reset()
        run.reset()

        for t in element_types:
            t._default_classes = default_classes[t]  # pylint: disable=protected-access
            t._default_style = default_styles[t]  # pylint: disable=protected-access
            t._default_props = default_props[t]  # pylint: disable=protected-access
        ui.markdown.default_extras = default_markdown_extras

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
