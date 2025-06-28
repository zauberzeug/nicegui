from __future__ import annotations

from starlette.datastructures import QueryParams

from .elements.sub_pages import SubPages


class PageArgs:
    """Container for page arguments like query parameters.

    This class provides access to request data for sub-page functions.
    Can be used as a parameter in sub-page functions and will be automatically injected.
    """

    def __init__(self, query_parameters: QueryParams, frame: SubPages) -> None:
        """Initialize PageArgs with query parameters and frame reference.

        :param query_parameters: Query parameters from the request
        :param frame: Reference to the ui.sub_pages element currently executing
        """
        self._query_parameters = query_parameters
        self._frame = frame

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
