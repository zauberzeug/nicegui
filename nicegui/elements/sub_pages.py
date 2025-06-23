import inspect
import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from typing_extensions import Self

from .. import background_tasks, helpers
from ..context import context
from ..dataclasses import KWONLY_SLOTS
from ..element import Element
from ..elements.label import Label
from ..functions.javascript import run_javascript


@dataclass(**KWONLY_SLOTS)
class RouteMatch:
    """Information about a matched route."""
    path: str
    '''The sub-path that actually matched (e.g., "/user/123")'''
    pattern: str
    '''The original route pattern (e.g., "/user/{id}")'''
    builder: Callable
    '''The function to call to build the page'''
    params: Dict[str, str]
    '''The extracted parameters (name -> value) from the path (e.g., ``{"id": "123"}``)'''


class SubPages(Element, component='sub_pages.js'):

    def __init__(self, routes: Optional[Dict[str, Callable]] = None, *, root_path: Optional[str] = None):
        """Sub Pages

        Create a sub pages element to handle client-side routing within a page.

        :param routes: dictionary mapping sub-page paths to page builder functions
        :param root_path: optional root path to strip from incoming paths (useful for non-root page mounts)
        """
        super().__init__()
        self._routes = routes or {}
        self._root_path = root_path
        self._on_routes_changed()
        if self._is_root():
            self.on('open', lambda e: self.show_and_update_history(e.args))
            self.on('navigate', lambda e: self._handle_navigate(e.args))

    def add(self, path: str, page: Callable) -> Self:
        """Add a new route to the sub pages.

        :param path: the path pattern to match (can include {param} placeholders)
        :param page: the callable to execute when the path is matched
            ({param} placeholders will be passed to the function parameters with same name)
        :return: self for method chaining
        """
        self._routes[path] = page
        self._on_routes_changed()
        return self

    def show(self, full_path: str) -> None:
        """Show the page for the given path.

        :param full_path: the path to navigate to (can be empty string for root path; trailing slash is ignored)
        """
        self.clear()
        with self:
            match_result = self.find_route_match(full_path)
            if match_result is None:
                Label(f'404: sub page {full_path} not found')
                return
            self._place_content(match_result)
            child_sub_pages = find_child_sub_pages_element(self)
            if child_sub_pages:
                child_sub_pages.show(full_path[len(match_result.path):])

    def show_and_update_history(self, path: str) -> None:
        """Show the page and update browser history.

        :param path: the path to navigate to
        """
        self.show(path)
        if self._is_root():
            run_javascript(f'''
                const fullPath = (window.path_prefix || '') + "{path}";
                if (window.location.pathname !== fullPath) {{
                    history.pushState({{page: "{path}"}}, "", fullPath);
                }}
            ''')

    def find_route_match(self, path: str) -> Optional[RouteMatch]:
        """Find the first matching route for a path with segment dropping.

        :return: RouteMatch object if found, None otherwise
        """
        normalized_path = self._normalize_path(path)
        segments = normalized_path.split('/')
        while segments:
            sub_path = '/'.join(segments)
            for route, builder in self._routes.items():
                matches = self._match_path(route, sub_path)
                if matches is not None:
                    return RouteMatch(path=sub_path, pattern=route, builder=builder, params=matches)
            segments.pop()
        return None

    def _on_routes_changed(self) -> None:
        if self._is_root():
            assert context.client.request
            path = context.client.request.url.path
            self.show_and_update_history(path)

    def _handle_navigate(self, path: str) -> None:
        """Handle navigate event from link clicks"""
        if not try_navigate_to_sub_page(path):
            context.client.open(path)

    def _normalize_path(self, path: str) -> str:
        """Normalize the path by trimming root path and handling trailing slashes."""
        if self._root_path is not None:
            root = self._root_path.rstrip('/')
            if path.startswith(root):
                path = path[len(root):]
        if path.endswith('/') and path != '/':
            path = path[:-1]
        if path == '':
            path = '/'
        return path

    @staticmethod
    def _match_path(pattern: str, path: str) -> Optional[Dict[str, str]]:
        """Match a path pattern against an actual path and extract parameters noted with {param} placeholders.

        :return: empty dict for exact matches, parameter dict for parameterized matches, None for no match.
        """
        if '{' not in pattern:
            return {} if pattern == path else None

        regex_pattern = re.escape(pattern)
        for match in re.finditer(r'\\{(\w+)\\}', regex_pattern):
            param_name = match.group(1)
            regex_pattern = regex_pattern.replace(f'\\{{{param_name}\\}}', f'(?P<{param_name}>[^/]+)')

        regex_match = re.match(f'^{regex_pattern}$', path)
        return regex_match.groupdict() if regex_match else None

    @staticmethod
    def _convert_parameter(value: str, param_type: type) -> Any:
        """Convert a string parameter to the specified type."""
        if param_type is str or param_type is inspect.Parameter.empty:
            return value
        elif param_type is int:
            return int(value)
        elif param_type is float:
            return float(value)
        elif param_type is bool:
            return value.lower() in ('true', '1', 'yes', 'on')
        return value

    def _is_root(self) -> bool:
        parent: Element = self
        while parent.parent_slot is not None:
            parent = parent.parent_slot.parent
            if isinstance(parent, SubPages):
                return False
        return True

    def _place_content(self, route_match: RouteMatch) -> None:
        if route_match.params:
            sig = inspect.signature(route_match.builder)
            converted_params = {
                name: self._convert_parameter(value, sig.parameters[name].annotation)
                for name, value in route_match.params.items()
                if name in sig.parameters
            }
            result = route_match.builder(**converted_params)
        else:
            result = route_match.builder()
        if helpers.is_coroutine_function(result):
            async def background_task():
                with self:
                    await result
            background_tasks.create(background_task(), name=f'building sub_page {route_match.pattern}')


def try_navigate_to_sub_page(path: str) -> bool:
    """Try to handle navigation through ``ui.sub_pages`` system.

    :param path: the path to navigate to
    :return: ``True`` if handled by ``ui.sub_pages``, ``False`` otherwise
    """
    try:
        client = context.client
        if client and client.content:
            sub_pages_elements = find_root_sub_pages_elements(client.content)
            handled_by_sub_pages = False
            for sub_page in sub_pages_elements:
                route_match = sub_page.find_route_match(path)
                if route_match is not None:
                    sub_page.show(path)
                    handled_by_sub_pages = True
            if handled_by_sub_pages:
                run_javascript(f'''
                    const fullPath = (window.path_prefix || '') + "{path}";
                    if (window.location.pathname !== fullPath) {{
                        history.pushState({{page: "{path}"}}, "", fullPath);
                    }}
                ''')
            return handled_by_sub_pages
    except (AttributeError, TypeError):
        pass
    return False


def find_root_sub_pages_elements(element: Element) -> List[SubPages]:
    """Find all root ui.sub_pages elements in an element tree.

    :param element: the element to search from
    :return: list of all root ui.sub_pages elements found
    """
    sub_pages_list = []

    def find_in_element(el: Element):
        if isinstance(el, SubPages) and el._is_root():  # pylint: disable=protected-access
            sub_pages_list.append(el)
        if hasattr(el, 'default_slot') and el.default_slot:
            for child in el.default_slot.children:
                find_in_element(child)

    find_in_element(element)
    return sub_pages_list


def find_child_sub_pages_element(element: Element) -> Optional[SubPages]:
    """Find child ui.sub_pages element, ensuring only one exists per level.

    :return: the ui.sub_pages element if found, None otherwise
    """
    for child in element.default_slot.children:
        if isinstance(child, SubPages):
            return child
        result = find_child_sub_pages_element(child)
        if result is not None:
            return result
    return None
