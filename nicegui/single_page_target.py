import inspect
import urllib.parse
from typing import Dict, Optional, TYPE_CHECKING, Self

if TYPE_CHECKING:
    from nicegui.single_page_router import SinglePageRouterEntry, SinglePageRouter


class SinglePageTarget:
    """Aa helper class which is used to parse the path and query parameters of an URL to  find the matching
    SinglePageRouterEntry and convert the parameters to the expected types of the builder function"""

    def __init__(self, path: Optional[str] = None, entry: Optional['SinglePageRouterEntry'] = None,
                 fragment: Optional[str] = None, query_string: Optional[str] = None,
                 router: Optional['SinglePageRouter'] = None):
        """
        :param path: The path of the URL
        :param entry: Predefined entry, e.g. targeting a Callable
        :param fragment: The fragment of the URL
        :param query_string: The query string of the URL
        :param router: The SinglePageRouter by which the URL was resolved
        """
        self.routes = {}  # all valid routes
        self.original_path = path
        self.path = path  # url path w/o query
        self.fragment = fragment
        self.query_string = query_string
        self.path_args = {}
        self.query_args = urllib.parse.parse_qs(self.query_string)
        self.entry = entry
        self.valid = entry is not None
        self.router = router

    def parse_single_page_route(self, routes: Dict[str, 'SinglePageRouterEntry'], path: str) -> Self:
        """
        :param routes: All routes of the single page router
        :param path: The path of the URL
        """
        parsed_url = urllib.parse.urlparse(urllib.parse.unquote(path))
        self.routes = routes  # all valid routes
        self.path = parsed_url.path  # url path w/o query
        self.fragment = parsed_url.fragment if len(parsed_url.fragment) > 0 else None
        self.query_string = parsed_url.query if len(parsed_url.query) > 0 else None
        self.path_args = {}
        self.query_args = urllib.parse.parse_qs(self.query_string)
        if self.fragment is not None and len(self.path) == 0:
            self.valid = True
            return self
        self.entry = self.parse_path()
        if self.entry is not None:
            self.convert_arguments()
            self.valid = True
        return self

    def parse_path(self) -> Optional['SinglePageRouterEntry']:
        """Splits the path into its components, tries to match it with the routes and extracts the path arguments
        into their corresponding variables.
        """
        for route, entry in self.routes.items():
            route_elements = route.lstrip('/').split('/')
            path_elements = self.path.lstrip('/').rstrip('/').split('/')
            if len(route_elements) != len(path_elements):  # can't match
                continue
            match = True
            for i, route_element_path in enumerate(route_elements):
                if route_element_path.startswith('{') and route_element_path.endswith('}') and len(
                        route_element_path) > 2:
                    self.path_args[route_element_path[1:-1]] = path_elements[i]
                elif path_elements[i] != route_element_path:
                    match = False
                    break
            if match:
                return entry
        return None

    def convert_arguments(self):
        """Converts the path and query arguments to the expected types of the builder function"""
        sig = inspect.signature(self.entry.builder)
        for func_param_name, func_param_info in sig.parameters.items():
            for params in [self.path_args, self.query_args]:
                if func_param_name in params:
                    if func_param_info.annotation is inspect.Parameter.empty:
                        continue
                    try:
                        params[func_param_name] = func_param_info.annotation(
                            params[func_param_name])  # Convert parameter to the expected type
                    except ValueError as e:
                        raise ValueError(f'Could not convert parameter {func_param_name}: {e}')
