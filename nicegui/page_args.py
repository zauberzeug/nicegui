from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .elements.sub_pages import SubPages

from starlette.datastructures import QueryParams


class PageArgs:
    """Container for page arguments like query parameters and path parameters.

    This class provides access to request data for sub-page functions.
    Can be used as a parameter in sub-page functions and will be automatically injected.
    """

    def __init__(self, query_parameters: QueryParams, path: str, frame: SubPages, path_parameters: dict[str, str], data: dict[str, Any]) -> None:
        """Initialize PageArgs with query parameters, frame reference, path parameters, and data.

        :param query_parameters: Query parameters from the request
        :param path: Path from the request
        :param frame: Reference to the ui.sub_pages element currently executing
        :param path_parameters: Path parameters extracted from the route pattern
        :param data: Arbitrary data passed to the sub_pages element
        """
        self._query_parameters = query_parameters
        self._path = path
        self._frame = frame
        self._path_parameters = path_parameters
        self._data = data

    @property
    def query_parameters(self) -> QueryParams:
        """Access to query parameters from the request URL.

        :return: QueryParams object containing the query parameters
        """
        return self._query_parameters

    @property
    def frame(self) -> SubPages:
        """Access to the ui.sub_pages element currently executing this page.

        :return: ui.sub_pages element that is rendering this page
        """
        return self._frame

    @property
    def path_parameters(self) -> dict[str, str]:
        """Access to path parameters extracted from the route pattern.

        :return: Dictionary containing path parameters as strings
        """
        return self._path_parameters

    @property
    def data(self) -> dict[str, Any]:
        """Access to arbitrary data passed to the ui.sub_pages element.

        :return: Dictionary containing the data passed to ui.sub_pages
        """
        return self._data
