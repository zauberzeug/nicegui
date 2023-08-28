from .. import globals  # pylint: disable=redefined-builtin


def add_body_html(code: str) -> None:
    globals.get_client().body_html += code + '\n'


def add_head_html(code: str) -> None:
    globals.get_client().head_html += code + '\n'
