from __future__ import annotations

from typing import TYPE_CHECKING

from ..context import context

if TYPE_CHECKING:
    from ..element import Element


def require_top_level_layout(element: Element) -> None:
    """Check if the element is a top level layout element."""
    parent = context.slot.parent
    if parent != parent.client.content:
        raise RuntimeError(
            f'Found top level layout element "{element.__class__.__name__}" inside element "{parent.__class__.__name__}". '
            'Top level layout elements can not be nested but must be direct children of the page content.',
        )
