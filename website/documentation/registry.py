from __future__ import annotations

from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from .model import Documentation

registry: Dict[str, Documentation] = {}


def add(documentation: Documentation) -> None:
    """Register a documentation."""
    registry[documentation.route] = documentation


def get(name: str) -> Documentation:
    """Get a documentation."""
    return registry[f'/documentation/{name}']
