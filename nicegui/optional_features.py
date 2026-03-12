import importlib.util
from typing import Literal

_optional_features: set[str] = set()

FEATURE = Literal[
    'altair',
    'anywidget',
    'highcharts',
    'matplotlib',
    'pandas',
    'pillow',
    'plotly',
    'polars',
    'pyecharts',
    'redis',
    'webview',
]


def register(feature: FEATURE) -> None:
    """Register an optional feature."""
    _optional_features.add(feature)


def try_register(feature: FEATURE, *, package: str | None = None) -> None:
    """Register an optional feature if the corresponding package is installed."""
    try:
        if importlib.util.find_spec(package or feature):
            _optional_features.add(feature)
    except (ModuleNotFoundError, ValueError):
        pass


def has(feature: FEATURE) -> bool:
    """Check if an optional feature is registered."""
    return feature in _optional_features
