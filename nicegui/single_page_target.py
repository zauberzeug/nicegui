import inspect
import urllib.parse
from typing import Dict, Optional, TYPE_CHECKING, Self, Callable

if TYPE_CHECKING:
    from nicegui.single_page_router_config import SinglePageRouterPath
    from nicegui.single_page_router import SinglePageRouter


class SinglePageTarget:
    """A helper class which is used to resolve and URL path and it's query and fragment parameters to find the matching
    SinglePageRouterPath and extract path and query parameters."""

    def __init__(self,
                 path: Optional[str] = None,
                 fragment: Optional[str] = None,
                 query_string: Optional[str] = None,
                 builder: Optional[Callable] = None,
                 title: Optional[str] = None,
                 router: Optional["SinglePageRouter"] = None,
                 router_path: Optional["SinglePageRouterPath"] = None):
        """
        :param builder: The builder function to be called when the URL is opened
        :param path: The path of the URL (to be shown in the browser)
        :param fragment: The fragment of the URL
        :param query_string: The query string of the URL
        :param title: The title of the URL to be displayed in the browser tab
        :param router: The SinglePageRouter which is used to resolve the URL
        :param router_path: The SinglePageRouterPath which is matched by the URL
        """
        self.original_path = path
        self.path = path
        self.path_args = {}
        self.path_elements = []
        self.fragment = fragment
        self.query_string = query_string
        self.query_args = urllib.parse.parse_qs(self.query_string)
        self.title = title
        self.builder = builder
        self.valid = builder is not None
        self.router = router
        self.router_path: Optional["SinglePageRouterPath"] = router_path
        if router_path is not None and router_path.builder is not None:
            self.builder = router_path.builder
            self.title = router_path.title
            self.valid = True

    def parse_url_path(self, routes: Dict[str, 'SinglePageRouterPath']) -> Self:
        """
        Parses the route using the provided routes dictionary and path.

        :param routes: All routes of the single page router
        """
        parsed_url = urllib.parse.urlparse(urllib.parse.unquote(self.path))
        self.path = parsed_url.path  # url path w/o query
        self.fragment = parsed_url.fragment if len(parsed_url.fragment) > 0 else None
        self.query_string = parsed_url.query if len(parsed_url.query) > 0 else None
        self.path_args = {}
        self.query_args = urllib.parse.parse_qs(self.query_string)
        if self.fragment is not None and len(self.path) == 0:
            self.valid = True
            return self
        entry = self.parse_path(routes)
        self.router_path = entry
        if entry is not None:
            self.builder = entry.builder
            self.title = entry.title
            self.convert_arguments()
            self.valid = True
        else:
            self.builder = None
            self.title = None
            self.valid = False
        return self

    def parse_path(self, routes) -> Optional['SinglePageRouterPath']:
        """Splits the path into its components, tries to match it with the routes and extracts the path arguments
        into their corresponding variables.

        :param routes: All valid routes of the single page router
        """
        path_elements = self.path.lstrip('/').rstrip('/').split('/')
        self.path_elements = path_elements
        for route, entry in routes.items():
            route_elements = route.lstrip('/').split('/')
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
        if not self.builder:
            return
        sig = inspect.signature(self.builder)
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
