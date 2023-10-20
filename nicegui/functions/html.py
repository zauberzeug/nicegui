from .. import context


def add_body_html(code: str) -> None:
    """Add HTML code to the body of the page."""
    context.get_client().body_html += code + '\n'


def add_head_html(code: str) -> None:
    """Add HTML code to the head of the page."""
    context.get_client().head_html += code + '\n'
