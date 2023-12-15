from .. import context, json


def page_title(title: str) -> None:
    """Page title

    Set the page title for the current client.

    :param title: page title
    """
    client = context.get_client()
    client.title = title
    if client.has_socket_connection:
        client.run_javascript(f'document.title = {json.dumps(title)}')
