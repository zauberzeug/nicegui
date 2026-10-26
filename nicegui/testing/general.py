import contextlib
import gc
import sys
import weakref
from copy import copy
from typing import cast

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
        if hasattr(route, 'original_router'):  # a router that FastAPI 0.141+ keeps as a single lazy route
            app.routes.remove(route)

    app.openapi_schema = None
    app.middleware_stack = None
    app.user_middleware.clear()
    app.urls.clear()
    core.reset()

    # weak keys, so that the snapshot does not keep element classes of earlier simulations alive
    element_defaults = weakref.WeakKeyDictionary({
        # pylint: disable-next=protected-access
        t: (copy(t._default_classes), copy(t._default_style), copy(t._default_props))
        for t in cast(list[type[ui.element]], [ui.element, *_find_all_subclasses(ui.element)])
    })
    default_markdown_extras = ui.markdown.default_extras[:]
    exception_handlers = dict(app.exception_handlers)

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

        for t, (classes, style, props) in element_defaults.items():
            t._default_classes = classes  # pylint: disable=protected-access
            t._default_style = style  # pylint: disable=protected-access
            t._default_props = props  # pylint: disable=protected-access
        ui.markdown.default_extras = default_markdown_extras
        app.exception_handlers = exception_handlers

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
