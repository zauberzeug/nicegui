from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .elements.sub_pages import SubPages

from starlette.datastructures import QueryParams

from .dataclasses import KWONLY_SLOTS


@dataclass(**KWONLY_SLOTS)
class PageArgs:
    """Container for page arguments like query parameters and path parameters.

    This class provides access to request data.
    It will be automatically injected into a sub-page builder function if the parameter is annotated with ``PageArgs``.
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
