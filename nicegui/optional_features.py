from typing import Set

_optional_features: Set[str] = set()


def register(feature: str) -> None:
    """Register an optional feature."""
    _optional_features.add(feature)


def has(feature: str) -> bool:
    """Check if an optional feature is registered."""
    return feature in _optional_features
