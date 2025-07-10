from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Dict, Union, get_args, get_origin

from starlette.datastructures import QueryParams

from .dataclasses import KWONLY_SLOTS

if TYPE_CHECKING:
    from .elements.sub_pages import SubPages


@dataclass(**KWONLY_SLOTS)
class RouteMatch:
    """Contains details about a matched route including path parameters and query data."""
    path: str
    '''The sub-path that actually matched (e.g., "/user/123")'''
    pattern: str
    '''The original route pattern (e.g., "/user/{id}")'''
    builder: Callable
    '''The function to call to build the page'''
    parameters: Dict[str, str]
    '''The extracted parameters (name -> value) from the path (e.g., ``{"id": "123"}``)'''
    query_params: QueryParams
    '''The query parameters from the URL'''
    fragment: str
    '''The URL fragment (e.g., "section" from "#section")'''

    @property
    def full_url(self) -> str:
        """Get the complete URL including path and query parameters, but excluding fragment.

        Fragments should not trigger page rebuilds, only scrolling behavior.
        """
        url = self.path
        if self.query_params:
            url += '?' + str(self.query_params)
        return url


@dataclass(**KWONLY_SLOTS)
class PageArgs:
    """Provides unified access to route data including path parameters and query parameters.

    Automatically injected into sub-page builder functions when the parameter is annotated with ``PageArgs``.
    """
    path: str
    '''Path from the request.'''
    frame: SubPages
    '''Reference to the ui.sub_pages element currently executing this page.'''
    path_parameters: dict[str, str]
    '''Path parameters extracted from the route pattern.'''
    query_parameters: QueryParams
    '''Query parameters from the request URL.'''
    data: dict[str, Any]
    '''Arbitrary data passed to the ui.sub_pages element.'''

    @classmethod
    def build_kwargs(cls, route_match: RouteMatch, frame: SubPages, data: dict[str, Any]) -> dict[str, Any]:
        """Build keyword arguments for the route builder function.

        :param route_match: matched route containing path info and parameters
        :param frame: SubPages instance executing this page
        :param data: arbitrary data passed to the sub_pages element
        :return: keyword arguments for the builder function
        """
        parameters = inspect.signature(route_match.builder).parameters
        kwargs = {}

        for name, param in parameters.items():
            if param.annotation is cls:
                kwargs[name] = cls._from_route_match(route_match, frame, data)
            elif name in data:
                kwargs[name] = data[name]
            elif route_match.parameters and name in route_match.parameters:
                kwargs[name] = cls._convert_parameter(route_match.parameters[name], param.annotation)
            elif name in route_match.query_params:
                kwargs[name] = cls._convert_parameter(route_match.query_params[name], param.annotation)

        return kwargs

    @classmethod
    def _from_route_match(cls, route_match: RouteMatch, frame: SubPages, data: dict[str, Any]) -> PageArgs:
        """Create a PageArgs instance from route match data.

        :param route_match: matched route containing path info and parameters
        :param frame: SubPages instance executing this page
        :param data: arbitrary data passed to the sub_pages element
        :return: new PageArgs instance
        """
        return cls(
            path=route_match.path,
            frame=frame,
            path_parameters=route_match.parameters or {},
            query_parameters=route_match.query_params,
            data=data
        )

    @staticmethod
    def _unwrap_optional(param_type: type) -> type:
        """Extract the base type from Optional[T] -> T, or return the type as-is."""
        if get_origin(param_type) is Union and type(None) in get_args(param_type):
            return next(arg for arg in get_args(param_type) if arg is not type(None))
        return param_type

    @staticmethod
    def _convert_parameter(value: str, param_type: type) -> Any:
        """Convert a string parameter to the specified type (``str``, ``int``, or ``float``).

        :param value: string value to convert
        :param param_type: target type for conversion
        :return: converted value
        """
        param_type = PageArgs._unwrap_optional(param_type)
        if param_type is str or param_type is inspect.Parameter.empty:
            return value
        elif param_type is int:
            return int(value)
        elif param_type is float:
            return float(value)
        return value
