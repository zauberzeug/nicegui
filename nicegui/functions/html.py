from .. import globals


def add_body_html(code: str) -> None:
    globals.client_stack[-1].body_html += code + '\n'


def add_head_html(code: str) -> None:
    globals.client_stack[-1].head_html += code + '\n'
