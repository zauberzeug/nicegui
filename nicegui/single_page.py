import inspect
import urllib.parse
from typing import Callable, Dict, Union, Optional, Tuple

from fastapi.routing import APIRoute

from nicegui import background_tasks, helpers, ui, core, Client, app

SPR_PAGE_BODY = '__pageContent'


class SinglePageRouterFrame(ui.element, component='single_page.js'):
    """The RouterFrame is a special element which is used by the SinglePageRouter to exchange the content of the
    current page with the content of the new page. It serves as container and overrides the browser's history
    management to prevent the browser from reloading the whole page."""

    def __init__(self, base_path: str):
        """
        :param base_path: The base path of the single page router which shall be tracked (e.g. when clicking on links)
        """
        super().__init__()
        self._props["base_path"] = base_path


class SinglePageRouterEntry:
    """The SinglePageRouterEntry is a data class which holds the configuration of a single page router route"""

    def __init__(self, path: str, builder: Callable, title: Union[str, None] = None):
        """
        :param path: The path of the route
        :param builder: The builder function which is called when the route is opened
        :param title: Optional title of the page
        """
        self.path = path
        self.builder = builder
        self.title = title


class UrlParameterResolver:
    """The UrlParameterResolver is a helper class which is used to resolve the path and query parameters of an URL to
    find the matching SinglePageRouterEntry and convert the parameters to the expected types of the builder function"""

    def __init__(self, routes: Dict[str, SinglePageRouterEntry], path: str):
        """
        :param routes: The routes of the single page router
        :param path: The path of the URL
        """
        components = path.split("?")
        path = components[0].rstrip("/")
        self.routes = routes
        self.query_string = components[1] if len(components) > 1 else ""
        self.query_args = {}
        self.path = path
        self.path_args = {}
        self.parse_query()
        self.entry = self.resolve_path()
        if self.entry is not None:
            self.convert_arguments()

    def resolve_path(self) -> Optional[SinglePageRouterEntry]:
        """Splits the path into its components, tries to match it with the routes and extracts the path arguments
        into their corresponding variables.

        :param path: The path to resolve
        """
        for route, entry in self.routes.items():
            route_elements = route.lstrip('/').split("/")
            path_elements = self.path.lstrip('/').split("/")
            if len(route_elements) != len(path_elements):  # can't match
                continue
            match = True
            for i, route_element_path in enumerate(route_elements):
                if route_element_path.startswith("{") and route_element_path.endswith("}") and len(
                        route_element_path) > 2:
                    self.path_args[route_element_path[1:-1]] = path_elements[i]
                elif path_elements[i] != route_element_path:
                    match = False
                    break
            if match:
                return entry
        return None

    def parse_query(self):
        """Parses the query string of the URL into a dictionary of key-value pairs"""
        self.query_args = urllib.parse.parse_qs(self.query_string)

    def convert_arguments(self):
        """Converts the path and query arguments to the expected types of the builder function"""
        sig = inspect.signature(self.entry.builder)
        for name, param in sig.parameters.items():
            for params in [self.path_args, self.query_args]:
                if name in params:
                    # Convert parameter to the expected type
                    try:
                        params[name] = param.annotation(params[name])
                    except ValueError as e:
                        raise ValueError(f"Could not convert parameter {name}: {e}")


class SinglePageRouter:
    """The SinglePageRouter allows the development of a Single Page Application (SPA) which maintains a
    persistent connection to the server and only updates the content of the page instead of reloading the whole page.

    This enables the development of complex web applications with dynamic per-user data (all types of Python classes)
    which are kept alive for the duration of the connection.

    Example:
        ```
        from nicegui import ui
        from nicegui.page import page
        from nicegui.single_page import SinglePageRouter

        @page('/', title="Welcome!")
        def index():
            ui.label("Welcome to the single page router example!")
            ui.link("About", "/about")

        @page('/about', title="About")
        def about():
            ui.label("This is the about page")
            ui.link("Index", "/")

        router = SinglePageRouter("/").setup_page_routes()
        ui.run()
        ```
    """

    def __init__(self, path: str, on_session_created: Optional[Callable] = None) -> None:
        """
        :param path: the base path of the single page router.
        :param on_session_created: Optional callback which is called when a new session is created.
        """
        super().__init__()
        self.routes: Dict[str, SinglePageRouterEntry] = {}
        self.base_path = path
        self._find_api_routes()
        self.content_area_class = SinglePageRouterFrame
        self.on_session_created: Optional[Callable] = on_session_created

    def setup_page_routes(self, **kwargs):
        """Registers the SinglePageRouter with the @page decorator to handle all routes defined by the router

        :param kwargs: Additional arguments for the @page decorators
        """

        @ui.page(self.base_path, **kwargs)
        @ui.page(f'{self.base_path}' + '{_:path}', **kwargs)  # all other pages
        async def root_page():
            self.handle_session_created()
            self.setup_root_page()

    def handle_session_created(self):
        """Is called when ever a new session is created such as when the user opens the page for the first time or
        in a new tab. Can be used to initialize session data"""
        if self.on_session_created is not None:
            self.on_session_created()

    def setup_root_page(self):
        """Builds the root page of the single page router and initializes the content area.

        Is only calling the setup_content_area method by default but can be overridden to customize the root page
        for example with a navigation bar, footer or embedding the content area within a container element.

        Example:
            ```
            def setup_root_page(self):
                app.storage.session["menu"] = ui.left_drawer()
                with app.storage.session["menu"] :
                    ... setup navigation
                with ui.column():
                    self.setup_content_area()
                ... footer
            ```
        """
        self.setup_content_area()

    def setup_content_area(self) -> SinglePageRouterFrame:
        """Setups the content area for the single page router

        :return: The content area element
        """
        content = self.content_area_class(self.base_path).on('open', lambda e: self.open(e.args))
        app.storage.session[SPR_PAGE_BODY] = content
        return content

    def add_page(self, path: str, builder: Callable, title: Optional[str] = None) -> None:
        """Add a new route to the single page router

        :param path: The path of the route
        :param builder: The builder function
        :param title: Optional title of the page
        """
        self.routes[path] = SinglePageRouterEntry(path.rstrip("/"), builder, title)

    def add_router_entry(self, entry: SinglePageRouterEntry) -> None:
        """Adds a fully configured SinglePageRouterEntry to the router

        :param entry: The SinglePageRouterEntry to add
        """
        self.routes[entry.path] = entry

    def get_router_entry(self, target: Union[Callable, str]) -> Tuple[Optional[SinglePageRouterEntry], dict, dict]:
        """Returns the SinglePageRouterEntry for the given target URL or builder function

        :param target: The target URL or builder function
        :return: The SinglePageRouterEntry or None if not found
        """
        if isinstance(target, Callable):
            for path, entry in self.routes.items():
                if entry.builder == target:
                    return entry, {}, {}
        else:
            target = target.rstrip("/")
            entry = self.routes.get(target, None)
            if entry is None:
                parser = UrlParameterResolver(self.routes, target)
                return parser.entry, parser.path_args, parser.query_args
            return entry, {}, {}

    def open(self, target: Union[Callable, str, Tuple[str, bool]]) -> None:
        """Open a new page in the browser by exchanging the content of the root page's slot element

        :param target: the target route or builder function. If a list is passed, the second element is a boolean
                        indicating whether the navigation should be server side only and not update the browser."""
        if isinstance(target, list):
            target, server_side = target  # unpack the list
        else:
            server_side = True
        entry, route_args, query_args = self.get_router_entry(target)
        title = entry.title if entry.title is not None else core.app.config.title
        ui.run_javascript(f'document.title = "{title}"')
        if server_side:
            ui.run_javascript(f'window.history.pushState({{page: "{target}"}}, "", "{target}");')

        async def build(content_element, kwargs) -> None:
            with content_element:
                result = entry.builder(**kwargs)
                if helpers.is_coroutine_function(entry.builder):
                    await result

        content = app.storage.session[SPR_PAGE_BODY]
        content.clear()
        combined_dict = {**route_args, **query_args}
        background_tasks.create(build(content, combined_dict))

    def _find_api_routes(self):
        """Find all API routes already defined via the @page decorator, remove them and redirect them to the
        single page router"""
        page_routes = set()
        for key, route in Client.page_routes.items():
            if (route.startswith(self.base_path) and
                    not route[len(self.base_path):].startswith("_")):
                page_routes.add(route)
                Client.single_page_routes[route] = self
                title = None
                if key in Client.page_configs:
                    title = Client.page_configs[key].title
                route = route.rstrip("/")
                self.routes[route] = SinglePageRouterEntry(route, builder=key, title=title)
        for route in core.app.routes.copy():
            if isinstance(route, APIRoute):
                if route.path in page_routes:
                    core.app.routes.remove(route)
