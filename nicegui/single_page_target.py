from __future__ import annotations

import inspect
import urllib.parse
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Self, get_args, get_origin

if TYPE_CHECKING:
    from nicegui.content import ContentPath
    from nicegui.single_page_router import SinglePageRouter


class SinglePageTarget:
    """A helper class which is used to resolve and URL path, it's query and fragment parameters to find the matching
    ContentPath and extract path and query parameters."""

    def __init__(self,
                 path: Optional[str] = None,
                 fragment: Optional[str] = None,
                 query_string: Optional[str] = None,
                 builder: Optional[Callable] = None,
                 title: Optional[str] = None,
                 router: Optional[SinglePageRouter] = None,
                 router_path: Optional[ContentPath] = None,
                 on_pre_update: Optional[Callable[[Any], None]] = None,
                 on_post_update: Optional[Callable[[Any], None]] = None
                 ):
        """
        :param builder: The builder function to be called when the URL is opened
        :param path: The path of the URL (to be shown in the browser)
        :param fragment: The fragment of the URL
        :param query_string: The query string of the URL
        :param title: The title of the URL to be displayed in the browser tab
        :param router: The SinglePageRouter which is used to resolve the URL
        :param router_path: The ContentPath which is matched by the URL
        :param on_pre_update: Optional callback which is called before content is updated. It can be used to modify the
            target or execute JavaScript code before the content is updated.
        :param on_post_update: Optional callback which is called after content is updated. It can be used to modify the
            target or execute JavaScript code after the content is updated, e.g. showing a message box or redirecting
            the user to another page.
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
        self.router_path: Optional[ContentPath] = router_path
        self.on_pre_update = on_pre_update
        self.on_post_update = on_post_update
        if router_path is not None and router_path.builder is not None:
            self.builder = router_path.builder
            self.title = router_path.title
            self.valid = True

    def parse_url_path(self, routes: Dict[str, ContentPath]) -> Self:
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

    def parse_path(self, routes) -> Optional[ContentPath]:
        """Splits the path into its components, tries to match it with the routes and extracts the path arguments
        into their corresponding variables.

        :param routes: All valid routes of the single page router"""
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
                    value = params[func_param_name]
                    expected_type = func_param_info.annotation

                    # Handle cases where expected_type is a generic type like list[str]
                    origin_type = get_origin(expected_type)
                    type_args = get_args(expected_type)

                    if isinstance(value, list):
                        if origin_type is list:
                            # Convert each element in the list to the specified type
                            element_type = type_args[0] if type_args else any
                            try:
                                params[func_param_name] = [
                                    element_type(item) for item in value
                                ]
                            except ValueError as e:
                                raise ValueError(
                                    f'Could not convert elements of parameter {func_param_name} to {element_type}: {e}'
                                ) from e
                        else:
                            # Expected type is not a list; take the first element
                            value = value[0]
                            try:
                                params[func_param_name] = expected_type(value)
                            except ValueError as e:
                                raise ValueError(f'Could not convert parameter {func_param_name}: {e}') from e
                    else:  # noqa: PLR5501
                        if origin_type is list:
                            # Value is not a list but expected a list; wrap value in a list
                            element_type = type_args[0] if type_args else any
                            try:
                                params[func_param_name] = [element_type(value)]
                            except ValueError as e:
                                raise ValueError(
                                    f'Could not convert parameter {func_param_name} to list[{element_type}]: {e}'
                                ) from e
                        else:
                            # Regular conversion
                            try:
                                params[func_param_name] = expected_type(value)
                            except ValueError as e:
                                raise ValueError(f'Could not convert parameter {func_param_name}: {e}') from e
