from __future__ import annotations

import functools
import inspect
import types
from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Union, get_args, get_origin

from starlette.datastructures import QueryParams

if TYPE_CHECKING:
    from .elements.sub_pages import SubPages


@dataclass(kw_only=True, slots=True)
class RouteMatch:
    """Contains details about a matched route including path parameters and query data."""
    path: str
    '''The sub-path that actually matched (e.g., "/user/123").'''
    pattern: str
    '''The original route pattern (e.g., "/user/{id}").'''
    builder: Callable
    '''The function to call to build the page.'''
    parameters: dict[str, str]
    '''The extracted parameters (name -> value) from the path (e.g., ``{'id': '123'}``).'''
    query_params: QueryParams
    '''The query parameters from the URL.'''
    fragment: str
    '''The URL fragment (e.g., "section" from "#section").'''
    remaining_path: str = ''
    '''The remaining path after the matched path.'''

    @property
    def full_url(self) -> str:
        """Get the complete URL including path and query parameters, but excluding fragment.

        Fragments should not trigger page rebuilds, only scrolling behavior.
        """
        url = self.path
        if self.query_params:
            url += '?' + str(self.query_params)
        return url

    def __repr__(self) -> str:
        return f'{self.path=}, {self.pattern=}, builder={self.builder.__name__}, {self.parameters=}, {self.query_params=}, {self.fragment=}, {self.remaining_path=}'


@dataclass(kw_only=True, slots=True)
class PageArguments:
    """Provides unified access to route data including path parameters and query parameters.

    Automatically injected into sub-page builder functions when the parameter is annotated with ``PageArguments``.
    """
    path: str
    '''Matched sub-path, relative to this ``ui.sub_pages`` element (e.g., "/user/123").'''
    frame: SubPages
    '''Reference to the ``ui.sub_pages`` element currently executing this page.'''
    path_parameters: dict[str, str]
    '''Path parameters extracted from the route pattern.'''
    query_parameters: QueryParams
    '''Query parameters from the request URL.'''
    data: dict[str, Any]
    '''Arbitrary data passed to the ``ui.sub_pages`` element.'''
    remaining_path: str = ''
    '''Remaining path after the matched route (useful for wildcard routing).

    ``path`` and ``remaining_path`` always add up to the path handled by this ``ui.sub_pages`` element,
    so the root route ``/`` leaves no leading slash while any other route keeps it
    (e.g. ``'/' + 'x/2/a'`` and ``'/sub' + '/x/2/a'``).
    '''

    @classmethod
    def build_kwargs(cls, match: RouteMatch, frame: SubPages, data: dict[str, Any]) -> dict[str, Any]:
        """Build keyword arguments for the route builder function.

        :param route_match: matched route containing path info and parameters
        :param frame: ``ui.sub_pages`` instance executing this page
        :param data: arbitrary data passed to the ``ui.sub_pages`` element
        :return: keyword arguments for the builder function
        """
        kwargs = {}
        for name, annotation in builder_annotations(match.builder).items():
            if annotation is cls:
                kwargs[name] = cls._from_route_match(match, frame, data)
            elif name in data:
                kwargs[name] = data[name]
            elif match.parameters and name in match.parameters:
                kwargs[name] = cls._convert_parameter(match.parameters[name], annotation)
            elif name in match.query_params:
                kwargs[name] = cls._convert_parameter(match.query_params[name], annotation)

        return kwargs

    @classmethod
    def _from_route_match(cls, route_match: RouteMatch, frame: SubPages, data: dict[str, Any]) -> PageArguments:
        """Create a PageArguments instance from route match data.

        :param route_match: matched route containing path info and parameters
        :param frame: SubPages instance executing this page
        :param data: arbitrary data passed to the sub_pages element
        :return: new PageArguments instance
        """
        return cls(
            path=route_match.path,
            frame=frame,
            path_parameters=route_match.parameters or {},
            query_parameters=route_match.query_params,
            data=data,
            remaining_path=route_match.remaining_path,
        )

    @staticmethod
    def _convert_parameter(value: str, param_type: type) -> Any:
        """Convert a string parameter to the specified type (``str``, ``int``, or ``float``).

        :param value: string value to convert
        :param param_type: target type for conversion
        :return: converted value
        """
        param_type = PageArguments._unwrap_optional(param_type)
        if param_type is str or param_type is inspect.Parameter.empty:
            return value
        elif param_type is int:
            return int(value)
        elif param_type is float:
            return float(value)
        return value

    @staticmethod
    def _unwrap_optional(param_type: type) -> type:
        """Extract the base type from T|None -> T, or return the type as-is."""
        if get_origin(param_type) in (Union, types.UnionType) and types.NoneType in get_args(param_type):
            return next(arg for arg in get_args(param_type) if arg is not types.NoneType)
        return param_type


def builder_annotations(builder: Callable) -> dict[str, Any]:
    """Map the parameter names of a page builder to their annotations.

    String annotations (e.g. due to ``from __future__ import annotations``) are evaluated individually
    in the builder's global namespace.
    Annotations that cannot be resolved (e.g. types imported only under ``TYPE_CHECKING``) are kept as strings.
    """
    func = builder
    while isinstance(func, functools.partial) or hasattr(func, '__wrapped__'):
        func = func.func if isinstance(func, functools.partial) else func.__wrapped__
    namespace = getattr(func, '__globals__', None) or {}

    annotations: dict[str, Any] = {}
    for name, param in inspect.signature(builder).parameters.items():
        annotations[name] = param.annotation
        if isinstance(param.annotation, str):
            try:
                annotations[name] = eval(param.annotation, namespace)  # pylint: disable=eval-used
            except Exception:
                pass
    return annotations
