from typing import Literal, Set

_optional_features: Set[str] = set()

FEATURE = Literal[
    'highcharts',
    'matplotlib',
    'pandas',
    'pillow',
    'plotly',
    'polars',
    'pyecharts',
    'redis',
    'sass',
    'webview',
]


def register(feature: FEATURE) -> None:
    """Register an optional feature."""
    _optional_features.add(feature)


def has(feature: FEATURE) -> bool:
    """Check if an optional feature is registered."""
    return feature in _optional_features
