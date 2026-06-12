from ..context import context


def status_code(code: int) -> None:
    """Status code

    Set the HTTP status code for the current page response.
    Must be called during page building, before the response is sent to the client.

    *Added in version 3.10.0*

    :param code: HTTP status code (e.g. 200, 404, 503)
    """
    if not 100 <= code <= 599:
        raise ValueError(f'Invalid HTTP status code: {code}')
    context.client.status_code = code
