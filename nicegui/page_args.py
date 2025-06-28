from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from starlette.datastructures import QueryParams


class PageArgs:
    """Container for page arguments like query parameters.

    This class provides access to request data for sub-page functions.
    Can be used as a parameter in sub-page functions and will be automatically injected.
    """

    def __init__(self, query_parameters: 'QueryParams') -> None:
        """Initialize PageArgs with query parameters.

        :param query_parameters: Query parameters from the request
        """
        self._query_parameters = query_parameters

    @property
    def query_parameters(self) -> 'QueryParams':
        """Access to query parameters from the request URL.

        :return: QueryParams object containing the query parameters
        """
        return self._query_parameters
