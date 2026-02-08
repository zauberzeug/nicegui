"""Helpers for nested dictionary/attribute binding paths."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

PropertyName = str | tuple[str, ...]


def _normalize_name(name: PropertyName) -> tuple[str, ...]:
    """Convert property name to normalized tuple format."""
    if isinstance(name, str):
        if not name:
            raise ValueError('Property name cannot be an empty string')
        return (name,)
    if not name:
        raise ValueError('Property name tuple cannot be empty')
    if not all(isinstance(key, str) for key in name):
        raise ValueError('Property name tuple must contain only strings')
    return name


def _display_name(name: PropertyName) -> str:
    """Return a human-readable representation of a property name."""
    return '->'.join(_normalize_name(name))


def _path_contains_dict(obj: Any, name: PropertyName) -> bool:
    """Check if the nested path traverses through any dict/Mapping."""
    if isinstance(obj, Mapping):
        return True
    name = _normalize_name(name)
    if len(name) == 1:
        return False
    try:
        current = obj
        for key in name[:-1]:
            if isinstance(current, Mapping):
                return True
            current = getattr(current, key)
        return isinstance(current, Mapping)
    except (KeyError, AttributeError, TypeError):
        return False
