import fnmatch
import re
from typing import Callable, Dict, Union, Optional, Tuple, Self, List, Set

from fastapi.routing import APIRoute

from nicegui import background_tasks, helpers, ui, core, context, Client
from nicegui.single_page_url import SinglePageUrl


class SinglePageRouterFrame(ui.element, component='single_page.js'):
    """The SinglePageRouterFrame is a special element which is used by the SinglePageRouter to exchange the content of
    the current page with the content of the new page. It serves as container and overrides the browser's history
    management to prevent the browser from reloading the whole page."""

    def __init__(self, valid_path_masks: list[str], use_browser_history: bool = True):
        """
        :param valid_path_masks: A list of valid path masks which shall be allowed to be opened by the router
        :param use_browser_history: Optional flag to enable or disable the browser history management. Default is True.
        """
        super().__init__()
        self._props["valid_path_masks"] = valid_path_masks
        self._props["browser_history"] = use_browser_history


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

    def verify(self) -> Self:
        """Verifies a SinglePageRouterEntry for correctness. Raises a ValueError if the entry is invalid."""
        path = self.path
        if "{" in path:
            # verify only a single open and close curly bracket is present
            elements = path.split("/")
            for cur_element in elements:
                if "{" in cur_element:
                    if cur_element.count("{") != 1 or cur_element.count("}") != 1 or len(cur_element) < 3 or \
                            not (cur_element.startswith("{") and cur_element.endswith("}")):
                        raise ValueError("Only simple path parameters are supported. /path/{value}/{another_value}\n"
                                         f"failed for path: {path}")
        return self


class SinglePageRouter:
    """The SinglePageRouter allows the development of a Single Page Application (SPA) which maintains a
    persistent connection to the server and only updates the content of the page instead of reloading the whole page.

    This allows faster page switches and a more dynamic user experience because instead of reloading the whole page,
    only the content area is updated. The SinglePageRouter is a high-level abstraction which manages the routing
    and content area of the SPA.

    For examples see examples/single_page_router"""

    def __init__(self,
                 path: str,
                 browser_history: bool = True,
                 included: Union[List[Union[Callable, str]], str, Callable] = "/*",
                 excluded: Union[List[Union[Callable, str]], str, Callable] = "",
                 on_instance_created: Optional[Callable] = None) -> None:
        """
        :param path: the base path of the single page router.
        :param browser_history: Optional flag to enable or disable the browser history management. Default is True.
        :param included: Optional list of masks and callables of paths to include. Default is "/*" which includes all.
        If you do not want to include all relative paths, you can specify a list of masks or callables to refine the
        included paths. If a callable is passed, it must be decorated with a page.
        :param excluded: Optional list of masks and callables of paths to exclude. Default is "" which excludes none.
        Explicitly included paths (without wildcards) and Callables are always included, even if they match an
        exclusion mask.
        :param on_instance_created: Optional callback which is called when a new instance is created. Each browser tab
        or window is a new instance. This can be used to initialize the state of the application.
        """
        super().__init__()
        self.routes: Dict[str, SinglePageRouterEntry] = {}
        self.base_path = path
        # list of masks and callables of paths to include
        self.included: List[Union[Callable, str]] = [included] if not isinstance(included, list) else included
        # list of masks and callables of paths to exclude
        self.excluded: List[Union[Callable, str]] = [excluded] if not isinstance(excluded, list) else excluded
        # low level system paths which are excluded by default
        self.system_excluded = ["/docs", "/redoc", "/openapi.json", "_*"]
        # set of all registered paths which were finally included for verification w/ mask matching in the browser
        self.included_paths: Set[str] = set()
        self.content_area_class = SinglePageRouterFrame
        self.on_instance_created: Optional[Callable] = on_instance_created
        self.use_browser_history = browser_history
        self._setup_configured = False

    def setup_page_routes(self, **kwargs):
        """Registers the SinglePageRouter with the @page decorator to handle all routes defined by the router

        :param kwargs: Additional arguments for the @page decorators
        """
        if self._setup_configured:
            raise ValueError("The SinglePageRouter is already configured")
        self._setup_configured = True
        self._update_masks()
        self._find_api_routes()

        @ui.page(self.base_path, **kwargs)
        @ui.page(f'{self.base_path}' + '{_:path}', **kwargs)  # all other pages
        async def root_page():
            self.handle_instance_created()
            self.setup_root_page()

    def handle_instance_created(self):
        """Is called when ever a new instance is created such as when the user opens the page for the first time or
        in a new tab"""
        if self.on_instance_created is not None:
            self.on_instance_created()

    def setup_root_page(self):
        """Builds the root page of the single page router and initializes the content area.

        Is only calling the setup_content_area method by default but can be overridden to customize the root page
        for example with a navigation bar, footer or embedding the content area within a container element.

        Example:
            ```
            def setup_root_page(self):
                with ui.left_drawer():
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
        content = self.content_area_class(
            list(self.included_paths), self.use_browser_history).on('open', lambda e: self.open(e.args))
        context.get_client().single_page_content = content
        return content

    def add_page(self, path: str, builder: Callable, title: Optional[str] = None) -> None:
        """Add a new route to the single page router

        :param path: The path of the route
        :param builder: The builder function
        :param title: Optional title of the page
        """
        self.routes[path] = SinglePageRouterEntry(path.rstrip("/"), builder, title).verify()

    def add_router_entry(self, entry: SinglePageRouterEntry) -> None:
        """Adds a fully configured SinglePageRouterEntry to the router

        :param entry: The SinglePageRouterEntry to add
        """
        self.routes[entry.path] = entry.verify()

    def get_target_url(self, path: Union[Callable, str]) -> SinglePageUrl:
        """Returns the SinglePageRouterEntry for the given URL path or builder function

        :param path: The URL path to open or a builder function
        :return: The SinglePageUrl object which contains the parsed route, query arguments and fragment
        """
        if isinstance(path, Callable):
            for path, entry in self.routes.items():
                if entry.builder == path:
                    return SinglePageUrl(entry=entry)
        else:
            parser = SinglePageUrl(path)
            return parser.parse_single_page_route(self.routes, path)

    def open(self, target: Union[Callable, str, Tuple[str, bool]]) -> None:
        """Open a new page in the browser by exchanging the content of the root page's slot element

        :param target: the target route or builder function. If a list is passed, the second element is a boolean
                        indicating whether the navigation should be server side only and not update the browser."""
        if isinstance(target, list):
            target, server_side = target  # unpack the list
        else:
            server_side = True
        target_url = self.get_target_url(target)
        entry = target_url.entry
        if entry is None:
            if target_url.fragment is not None:
                ui.run_javascript(f'window.location.href = "#{target_url.fragment}";')  # go to fragment
                return
            return
        title = entry.title if entry.title is not None else core.app.config.title
        ui.run_javascript(f'document.title = "{title}"')
        if server_side and self.use_browser_history:
            ui.run_javascript(f'window.history.pushState({{page: "{target}"}}, "", "{target}");')

        async def build(content_element, fragment, kwargs) -> None:
            with content_element:
                result = entry.builder(**kwargs)
                if helpers.is_coroutine_function(entry.builder):
                    await result
                if fragment is not None:
                    await ui.run_javascript(f'window.location.href = "#{fragment}";')

        content = context.get_client().single_page_content
        content.clear()
        combined_dict = {**target_url.path_args, **target_url.query_args}
        background_tasks.create(build(content, target_url.fragment, combined_dict))

    def _is_excluded(self, path: str) -> bool:
        """Checks if a path is excluded by the exclusion masks

        :param path: The path to check
        :return: True if the path is excluded, False otherwise"""
        for element in self.included:
            if path == element:  # if it is a perfect, explicit match: allow
                return False
            if fnmatch.fnmatch(path, element):  # if it is just a mask match: verify it is not excluded
                for ex_element in self.excluded:
                    if fnmatch.fnmatch(path, ex_element):
                        return True  # inclusion mask matched but also exclusion mask
                return False  # inclusion mask matched
        return True  # no inclusion mask matched

    def _update_masks(self) -> None:
        """Updates the inclusion and exclusion masks and resolves Callables to the actual paths"""
        for cur_list in [self.included, self.excluded]:
            for index, element in enumerate(cur_list):
                if isinstance(element, Callable):
                    if element in Client.page_routes:
                        cur_list[index] = Client.page_routes[element]
                    else:
                        raise ValueError(
                            f"Invalid target page in inclusion/exclusion list, no @page assigned to element")

    def _find_api_routes(self) -> None:
        """Find all API routes already defined via the @page decorator, remove them and redirect them to the
        single page router"""
        page_routes = set()
        for key, route in Client.page_routes.items():
            if route.startswith(self.base_path) and not self._is_excluded(route):
                page_routes.add(route)
                Client.single_page_routes[route] = self
                title = None
                if key in Client.page_configs:
                    title = Client.page_configs[key].title
                route = route.rstrip("/")
                self.add_router_entry(SinglePageRouterEntry(route, builder=key, title=title))
                # /site/{value}/{other_value} --> /site/*/* for easy matching in JavaScript
                route_mask = re.sub(r'{[^}]+}', '*', route)
                self.included_paths.add(route_mask)
        for route in core.app.routes.copy():
            if isinstance(route, APIRoute):
                if route.path in page_routes:
                    core.app.routes.remove(route)
