import inspect
import re
from asyncio import iscoroutine
from typing import Any, Callable, Dict, Optional

from typing_extensions import Self

from .. import background_tasks
from ..context import context
from ..element import Element
from ..elements.label import Label
from ..functions.javascript import run_javascript


class SubPages(Element, component='sub_pages.js'):

    def __init__(self, routes: Optional[Dict[str, Callable]] = None):
        super().__init__()
        self._routes = routes or {}
        self._on_new_route()

    def add(self, path: str, page: Callable) -> Self:
        """Add a new route to the sub pages.

        :param path: the path pattern to match (can include {param} placeholders)
        :param page: the callable to execute when the path is matched
            ({param} placeholders will be passed to the function parameters with same name)
        :return: self for method chaining
        """
        self._routes[path] = page
        if path == '/':
            self._on_new_route()
        return self

    def show(self, full_path: str) -> None:
        """Show the page for the given path.

        :param full_path: the path to navigate to (can be empty string for root path; trailing slash is ignored)
        """
        if full_path.endswith('/') and full_path != '/':
            full_path = full_path[:-1]
        if full_path == '':
            full_path = '/'
        segments = full_path.split('/')
        while segments:
            sub_path = '/'.join(segments)
            for route, builder in self._routes.items():
                matches = self._match_path(route, sub_path)
                if matches is not None:
                    self._replace_content(route, builder, matches)
                    child_sub_pages = find_child_sub_pages_element(self)
                    if child_sub_pages:
                        child_sub_pages.show(full_path[len(sub_path):])
                    return
            segments.pop()
        self.clear()
        with self:
            Label(f'404: sub page {full_path} not found')

    def show_and_update_history(self, path: str) -> None:
        """Show the page and update browser history if successful.

        :param path: the path to navigate to
        """
        self.show(path)
        if self._is_root():
            run_javascript(f'''
                if (window.location.pathname !== "{path}") {{
                    history.pushState({{page: "{path}"}}, "", "{path}");
                }}
            ''')

    def _on_new_route(self) -> None:
        if self._is_root():
            assert context.client.request
            path = context.client.request.url.path
            self.show_and_update_history(path)
            self.on('open', lambda e: self.show(e.args))

    @staticmethod
    def _match_path(pattern: str, path: str) -> Optional[Dict[str, str]]:
        """Match a path pattern against an actual path and extract parameters noted with {param} placeholders.

        :return: empty dict for exact matches, parameter dict for parameterized matches, None for no match.
        """
        if '{' not in pattern:
            return {} if pattern == path else None
        regex_pattern = pattern
        for match in re.finditer(r'\{(\w+)\}', pattern):
            param_name = match.group(1)
            regex_pattern = regex_pattern.replace(f'{{{param_name}}}', f'(?P<{param_name}>[^/]+)')
        regex_pattern = f'^{regex_pattern}$'
        regex_match = re.match(regex_pattern, path)
        if regex_match:
            return regex_match.groupdict()
        return None

    def _convert_parameter(self, value: str, param_type: type) -> Any:
        """Convert a string parameter to the specified type."""
        if param_type is str:
            return value
        elif param_type is int:
            return int(value)
        elif param_type is float:
            return float(value)
        elif param_type is bool:
            return value.lower() in ('true', '1', 'yes', 'on')
        else:
            return value

    def _is_root(self) -> bool:
        parent: Element = self
        while parent.parent_slot is not None:
            parent = parent.parent_slot.parent
            if isinstance(parent, SubPages):
                return False
        return True

    def _replace_content(self, path: str, builder: Callable, params: Optional[Dict[str, str]] = None) -> None:
        self.clear()
        with self:
            if params:
                sig = inspect.signature(builder)
                converted_params = {}
                for param_name, param_value in params.items():
                    if param_name in sig.parameters:
                        param_info = sig.parameters[param_name]
                        param_type = param_info.annotation
                        if param_type != inspect.Parameter.empty:
                            converted_params[param_name] = self._convert_parameter(param_value, param_type)
                        else:
                            converted_params[param_name] = param_value
                result = builder(**converted_params)
            else:
                result = builder()
        if iscoroutine(result):
            async def background_task():
                with self:
                    await result
            background_tasks.create(background_task(), name=f'building sub_page {path}')


def find_root_sub_pages_element(element: Element) -> Optional[SubPages]:
    """Find the root ui.sub_pages element in an element tree.

    :param element: the element to search from
    :return: the root ui.sub_pages element if found, None otherwise
    """
    def find_in_element(el: Element):
        if isinstance(el, SubPages) and el._is_root():  # pylint: disable=protected-access
            return el
        if hasattr(el, 'default_slot') and el.default_slot:
            for child in el.default_slot.children:
                result = find_in_element(child)
                if result:
                    return result
        return None

    return find_in_element(element)


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
