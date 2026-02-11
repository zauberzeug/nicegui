from ..context import context


def status_code(code: int) -> None:
    """Status code

    Set the HTTP status code for the current page response.

    :param code: HTTP status code (e.g. 200, 404, 503)
    """
    context.client.status_code = code
