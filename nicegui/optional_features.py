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


def has(feature: FEATURE) -> bool:
    """Check if an optional feature is registered."""
    return feature in _optional_features
