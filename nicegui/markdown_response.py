from __future__ import annotations

from typing import TYPE_CHECKING

from starlette.responses import Response

if TYPE_CHECKING:
    from .client import Client


def build_markdown_response(client: Client, status_code: int = 200) -> Response:
    """Build a markdown response from the client's element tree."""
    parts = []
    title = client.resolve_title()
    if title:
        parts.append(f'# {title}')
    md = client.layout._render_markdown()  # pylint: disable=protected-access
    if md:
        parts.append(md)
    content = '\n\n'.join(parts)
    return Response(
        content=content,
        media_type='text/markdown; charset=utf-8',
        status_code=status_code,
        headers={
            'Cache-Control': 'no-store',
            # X-NiceGUI-Content lets clients programmatically distinguish NiceGUI page responses
            # from other responses (e.g. static files, API endpoints) without parsing the body.
            'X-NiceGUI-Content': 'page',
        },
    )
