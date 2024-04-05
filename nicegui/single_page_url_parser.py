import inspect
import urllib.parse
from typing import Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from nicegui.single_page import SinglePageRouterEntry


class UrlParser:
    """Aa helper class which is used to parse the path and query parameters of an URL to  find the matching
    SinglePageRouterEntry and convert the parameters to the expected types of the builder function"""

    def __init__(self, routes: Dict[str, "SinglePageRouterEntry"], path: str):
        """
        :param routes: The routes of the single page router
        :param path: The path of the URL
        """
        parsed_url = urllib.parse.urlparse(urllib.parse.unquote(path))
        self.routes = routes  # all valid routes
        self.path = parsed_url.path  # url path w/o query
        self.query_string = parsed_url.query
        self.path_args = {}
        self.query_args = urllib.parse.parse_qs(self.query_string)
        self.entry = self.parse_path()
        if self.entry is not None:
            self.convert_arguments()

    def parse_path(self) -> Optional["SinglePageRouterEntry"]:
        """Splits the path into its components, tries to match it with the routes and extracts the path arguments
        into their corresponding variables.
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

    def convert_arguments(self):
        """Converts the path and query arguments to the expected types of the builder function"""
        sig = inspect.signature(self.entry.builder)
        for func_param_name, func_param_info in sig.parameters.items():
            for params in [self.path_args, self.query_args]:
                if func_param_name in params:
                    try:
                        params[func_param_name] = func_param_info.annotation(
                            params[func_param_name])  # Convert parameter to the expected type
                    except ValueError as e:
                        raise ValueError(f"Could not convert parameter {func_param_name}: {e}")
