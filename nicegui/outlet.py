import fnmatch
import re
from functools import wraps
from typing import Callable, Dict, Union, Optional, Tuple, Self, List, Set, Any, Generator

from fastapi.routing import APIRoute

from nicegui import background_tasks, helpers, ui, core, context
from nicegui.elements.router_frame import RouterFrame
from nicegui.router_frame_url import SinglePageTarget


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
        if '{' in path:
            # verify only a single open and close curly bracket is present
            elements = path.split('/')
            for cur_element in elements:
                if '{' in cur_element:
                    if cur_element.count('{') != 1 or cur_element.count('}') != 1 or len(cur_element) < 3 or \
                            not (cur_element.startswith('{') and cur_element.endswith('}')):
                        raise ValueError('Only simple path parameters are supported. /path/{value}/{another_value}\n'
                                         f'failed for path: {path}')
        return self


class SinglePageRouteFrame:
    def open(self, target: Union[Callable, str, Tuple[str, bool]]) -> None:
        """Open a new page in the browser by exchanging the content of the root page's slot element

        :param target: the target route or builder function. If a list is passed, the second element is a boolean
                        indicating whether the navigation should be server side only and not update the browser."""
        if isinstance(target, list):
            target, server_side = target


class Outlet:
    """The SinglePageRouter allows the development of a Single Page Application (SPA) which maintains a
    persistent connection to the server and only updates the content of the page instead of reloading the whole page.

    This allows faster page switches and a more dynamic user experience because instead of reloading the whole page,
    only the content area is updated. The SinglePageRouter is a high-level abstraction which manages the routing
    and content area of the SPA.

    For examples see examples/single_page_router"""

    def __init__(self,
                 path: str,
                 browser_history: bool = True,
                 included: Union[List[Union[Callable, str]], str, Callable] = '/*',
                 excluded: Union[List[Union[Callable, str]], str, Callable] = '',
                 on_instance_created: Optional[Callable] = None,
                 **kwargs) -> None:
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
        :param kwargs: Additional arguments for the @page decorators
        """
        super().__init__()
        self.routes: Dict[str, SinglePageRouterEntry] = {}
        self.base_path = path
        # list of masks and callables of paths to include
        self.included: List[Union[Callable, str]] = [included] if not isinstance(included, list) else included
        # list of masks and callables of paths to exclude
        self.excluded: List[Union[Callable, str]] = [excluded] if not isinstance(excluded, list) else excluded
        # low level system paths which are excluded by default
        self.system_excluded = ['/docs', '/redoc', '/openapi.json', '_*']
        # set of all registered paths which were finally included for verification w/ mask matching in the browser
        self.included_paths: Set[str] = set()
        self.on_instance_created: Optional[Callable] = on_instance_created
        self.use_browser_history = browser_history
        self._setup_configured = False
        self.outlet_builder: Optional[Callable] = None
        self.page_kwargs = kwargs

    def __call__(self, func: Callable[..., Any]) -> Self:
        """Decorator for the outlet function"""
        self.outlet_builder = func
        self._setup_routing_pages()
        return self

    def _setup_routing_pages(self):
        @ui.page(self.base_path, **self.page_kwargs)
        @ui.page(f'{self.base_path}' + '{_:path}', **self.page_kwargs)  # all other pages
        async def root_page():
            self._setup_content_area()

    def view(self, path: str) -> 'OutletView':
        """Decorator for the view function"""
        return OutletView(path, self)

    def setup_page_routes(self, **kwargs):
        """Registers the SinglePageRouter with the @page decorator to handle all routes defined by the router

        :param kwargs: Additional arguments for the @page decorators
        """
        if self._setup_configured:
            raise ValueError('The SinglePageRouter is already configured')
        self._setup_configured = True
        self._update_masks()
        self._find_api_routes()

    def add_page(self, path: str, builder: Callable, title: Optional[str] = None) -> None:
        """Add a new route to the single page router

        :param path: The path of the route
        :param builder: The builder function
        :param title: Optional title of the page
        """
        self.included_paths.add(path.rstrip('/'))
        self.routes[path] = SinglePageRouterEntry(path, builder, title).verify()

    def add_router_entry(self, entry: SinglePageRouterEntry) -> None:
        """Adds a fully configured SinglePageRouterEntry to the router

        :param entry: The SinglePageRouterEntry to add
        """
        self.routes[entry.path] = entry.verify()

    def resolve_target(self, target: Union[Callable, str]) -> SinglePageTarget:
        """Tries to resolve a target such as a builder function or an URL path w/ route and query parameters.

        :param target: The URL path to open or a builder function
        :return: The resolved target. Defines .valid if the target is valid
        """
        if isinstance(target, Callable):
            for target, entry in self.routes.items():
                if entry.builder == target:
                    return SinglePageTarget(entry=entry)
        else:
            parser = SinglePageTarget(target)
            return parser.parse_single_page_route(self.routes, target)

    def navigate_to(self, target: Union[Callable, str, SinglePageTarget]) -> bool:
        """Navigate to a target

        :param target: The target to navigate to
        """
        if not isinstance(target, SinglePageTarget):
            target = self.resolve_target(target)
        if not target.valid:
            return False
        # TODO find right content area
        return True

    def _setup_content_area(self):
        """Setups the content area for the single page router

        :return: The content area element
        """
        frame = self.outlet_builder()
        next(frame)  # execute top layout components till first yield
        content = RouterFrame(list(self.included_paths), self.use_browser_history)  # exchangeable content of the page
        content.on_resolve(self.resolve_target)
        while True:  # execute the rest of the outlets ui setup yield by yield
            try:
                next(frame)
            except StopIteration:
                break

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
        from nicegui.page import Client
        for cur_list in [self.included, self.excluded]:
            for index, element in enumerate(cur_list):
                if isinstance(element, Callable):
                    if element in Client.page_routes:
                        cur_list[index] = Client.page_routes[element]
                    else:
                        raise ValueError(
                            f'Invalid target page in inclusion/exclusion list, no @page assigned to element')

    def _find_api_routes(self) -> None:
        """Find all API routes already defined via the @page decorator, remove them and redirect them to the
        single page router"""
        from nicegui.page import Client
        page_routes = set()
        for key, route in Client.page_routes.items():
            if route.startswith(self.base_path) and not self._is_excluded(route):
                page_routes.add(route)
                Client.single_page_routes[route] = self
                title = None
                if key in Client.page_configs:
                    title = Client.page_configs[key].title
                route = route.rstrip('/')
                self.add_router_entry(SinglePageRouterEntry(route, builder=key, title=title))
                # /site/{value}/{other_value} --> /site/*/* for easy matching in JavaScript
                route_mask = re.sub(r'{[^}]+}', '*', route)
                self.included_paths.add(route_mask)
        for route in core.app.routes.copy():
            if isinstance(route, APIRoute):
                if route.path in page_routes:
                    core.app.routes.remove(route)


class OutletView:

    def __init__(self, path: str, parent_outlet: Outlet):
        self.path = path
        self.parent_outlet = parent_outlet

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        self.parent_outlet.add_page(
            self.parent_outlet.base_path.rstrip('/') + self.path, func)
        return func
